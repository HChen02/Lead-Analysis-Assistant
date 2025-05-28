from flask import Flask, render_template, request, jsonify, send_from_directory, Response, redirect, url_for, session
import os
import re
import csv
import pandas as pd
import json
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain.callbacks.base import BaseCallbackHandler
import secrets  # Para generar secret_key
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Callback handler para respuestas streaming mejorado
class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.text = ""
        
    def on_llm_new_token(self, token, **kwargs):
        self.text += token
        return token


# Crear la aplicación Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = secrets.token_hex(16)  # Necesario para gestionar sesiones

# --- Cargar y fusionar datos ---
# Verifica si los archivos existen; si no, usa datos vacíos en modo de demostración
try:
    shap_df = pd.read_csv("shap_values.csv")
    pred_df = pd.read_csv("prediction.csv")
    DESCRIPTION_PATH = "description_crm_data.csv"
    data_df = pd.merge(shap_df, pred_df, on="id")
    valid_ids = set(data_df["id"].astype(str))
    data_loaded = True
except Exception as e:
    print(f"Error cargando datos: {e}")
    data_df = pd.DataFrame()
    valid_ids = set()
    data_loaded = False


# --- Inicializar el LLM local ---
try:
    # Aumentar num_predict para respuestas más largas
    llm = Ollama(model="gemma3:4b", temperature=0.0, num_predict=2048)
    llm_available = True
except Exception as e:
    print(f"Error inicializando Ollama: {e}")
    llm_available = False


# Esta función para inicializar la base de datos
def init_db():
    """Inicializa la base de datos SQLite para almacenar usuarios."""
    conn = sqlite3.connect('lead_assistant.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        company TEXT,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

def create_default_admin():
    """Crea un usuario administrador por defecto si no existe ningún usuario."""
    conn = sqlite3.connect('lead_assistant.db')
    cursor = conn.cursor()
    
    # Verificar si ya existe algún usuario
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Crear usuario administrador por defecto
        admin_name = "Administrador"
        admin_email = "admin@leadanalysis.com"
        admin_password = "admin123"  # En producción usar una contraseña más segura
        admin_company = "Lead Analysis Assistant"
        created_at = datetime.now().isoformat()
        
        password_hash = generate_password_hash(admin_password)
        
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, company, created_at) VALUES (?, ?, ?, ?, ?)",
            (admin_name, admin_email, password_hash, admin_company, created_at)
        )
        conn.commit()
        print(f"Usuario administrador creado: {admin_email} / {admin_password}")
    
    conn.close()


# --- Generar explicación textual ---
def generar_explicacion_textual(row, top_n=5):
    # Diccionario para almacenar descripciones de variables
    descripciones_vars = {}
    # Read the CSV and update the dictionary
    with open(DESCRIPTION_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row_des in reader:
            variable = row_des["Variable"].strip()
            descripcion = row_des["Descripción"].strip()
            descripciones_vars[variable] = descripcion
    if not data_loaded:
        return "No hay datos disponibles para generar una explicación."
    
    shap_values = row.drop(["id", "score", "rating", "user_id", "prediction_date"], errors='ignore')
    importantes = shap_values.abs().sort_values(ascending=False).head(top_n).index.tolist()
    razones = []
    for var in importantes:
        valor = shap_values[var]
        efecto = "aumentó" if valor > 0 else "redujo"
        descripcion = descripciones_vars.get(var, var)
        razones.append(
            f"{descripcion.capitalize()} {efecto} la puntuación estimada del contacto."
        )
    explicacion = (
        f"Este lead tiene ID {row['id']}. Su puntuación de compra fue clasificada como '{row['rating']}'. "
        f"Los factores más influyentes fueron: {'. '.join(razones)}"
    )
    return explicacion

# --- Cargar o crear índice FAISS ---
index_path = "faiss_index"
vector_store = None
embedding_model = None
qa_chain = None

def inicializar_rag():
    global vector_store, embedding_model, qa_chain
    
    if not data_loaded:
        return False
    
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        try:
            vector_store = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        except Exception:
            docs = [Document(page_content=generar_explicacion_textual(row), metadata={"id": row["id"]}) 
                   for _, row in data_df.iterrows()]
            vector_store = FAISS.from_documents(docs, embedding_model)
            vector_store.save_local(index_path)

        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, verbose=False)
        return True
    except Exception as e:
        print(f"Error inicializando RAG: {e}")
        return False

if data_loaded and llm_available:
    rag_available = inicializar_rag()
else:
    rag_available = False

# --- Extraer IDs y otras utilidades ---
def extraer_id_valido(pregunta: str):
    if not data_loaded:
        return None
        
    posibles = re.findall(r"\b[\w]+__\d{14}\b", pregunta)
    for pid in posibles:
        if pid in valid_ids:
            return pid
    return None

def es_saludo(texto: str):
    texto = texto.lower()
    saludos = ["hola", "buenas", "qué puedes hacer", "ayuda", "hey", "funcionalidad", "funciones", "hacer"]
    return any(s in texto for s in saludos)

def explicar_sistema(pregunta: str, stream=False):
    if not llm_available:
        return "Lo siento, el sistema LLM no está disponible en este momento."
    
    prompt = (
        "Eres un asistente que ayuda a usuarios de negocio a entender "
        "por qué ciertos leads tienen más potencial de compra que otros. "
        "Responde de forma clara y en español, sin tecnicismos innecesarios.\n\n"
        f"Pregunta del usuario: {pregunta}\n\n"
        "Si te preguntan sobre la funcionalidad del sistema, explica que: "
        "Este chatbot está diseñado para analizar leads (contactos comerciales potenciales) "
        "y explicar qué factores influyen en su puntuación de potencial de compra. "
        "Puedes preguntar sobre leads específicos usando su ID, o hacer preguntas generales "
        "sobre factores que influyen en las puntuaciones de los leads."
    )
    
    if stream:
        # Para streaming, usar el modelo con capacidad para respuestas más largas
        streaming_llm = Ollama(model="gemma3:4b", temperature=0.0, num_predict=2048)
        
        # Función generadora para enviar tokens a medida que llegan
        def generate():
            try:
                for chunk in streaming_llm.stream(prompt):
                    yield f"data: {json.dumps({'token': chunk})}\n\n"
                # Asegurar que se envía una señal clara de finalización
                yield "data: {\"token\": \"\\n\"}\n\n"  # Añadir un salto de línea al final
                yield "data: [DONE]\n\n"
            except Exception as e:
                print(f"Error en stream: {e}")
                yield f"data: {json.dumps({'token': '\\nError en streaming: Intenta recargar la página.'})}\n\n"
                yield "data: [DONE]\n\n"
        
        return generate
    else:
        # Para respuestas completas (no streaming)
        try:
            return llm.invoke(prompt)
        except Exception as e:
            print(f"Error en LLM: {e}")
            return "Lo siento, ocurrió un error al procesar tu consulta. Por favor, intenta de nuevo."

# --- NUEVA FUNCIÓN: Agregar nuevo lead al sistema ---
def agregar_nuevo_lead(lead_data):
    """
    Agrega un nuevo lead al sistema y actualiza el índice FAISS.
    
    Args:
        lead_data (dict): Diccionario con los datos del nuevo lead.
                         Debe incluir al menos 'id', 'rating' y los valores SHAP.
    
    Returns:
        bool: True si el lead se agregó correctamente, False en caso contrario.
    """
    global data_df, valid_ids, vector_store
    
    if not data_loaded or not rag_available:
        return False
    
    try:
        # Verificar que el ID no exista ya
        lead_id = lead_data.get('id')
        if lead_id in valid_ids:
            print(f"El lead con ID {lead_id} ya existe.")
            return False
        
        # Convertir el diccionario a DataFrame
        new_lead_df = pd.DataFrame([lead_data])
        
        # Añadir al DataFrame principal
        data_df = pd.concat([data_df, new_lead_df], ignore_index=True)
        
        # Actualizar el conjunto de IDs válidos
        valid_ids.add(str(lead_id))
        
        # Generar explicación textual para este lead
        lead_row = data_df[data_df['id'] == lead_id].iloc[0]
        explanation = generar_explicacion_textual(lead_row)
        
        # Crear nuevo documento para el índice FAISS
        new_doc = Document(page_content=explanation, metadata={"id": lead_id})
        
        # Añadir al índice FAISS
        vector_store.add_documents([new_doc])
        
        # Opcionalmente, guardar el índice actualizado
        vector_store.save_local(index_path)
        
        # Actualizar los archivos CSV (opcional, dependiendo de si quieres persistencia)
        # Esto requeriría separar los datos en los formatos correspondientes de shap_df y pred_df
        
        print(f"Lead con ID {lead_id} agregado correctamente.")
        return True
    
    except Exception as e:
        print(f"Error al agregar nuevo lead: {e}")
        return False

# --- Rutas de la aplicación ---

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def login():
    """Ruta principal que muestra la página de login"""
    # Si el usuario ya tiene una sesión activa, redirigir al dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Ruta del dashboard que muestra la interfaz del chatbot"""
    # Verificar si el usuario tiene una sesión activa
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', 
                          data_loaded=data_loaded, 
                          llm_available=llm_available,
                          rag_available=rag_available)

@app.route('/api/login', methods=['POST'])
def api_login():
    """Endpoint para procesar el inicio de sesión"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({
            'success': False,
            'message': 'Por favor, ingresa tu correo y contraseña.'
        }), 400
    
    try:
        conn = sqlite3.connect('lead_assistant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[3], password):
            # Actualizar última fecha de inicio de sesión
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now().isoformat(), user[0])
            )
            conn.commit()
            conn.close()
            
            # Guardar datos del usuario en la sesión
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            
            return jsonify({'success': True})
        else:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Credenciales incorrectas'
            }), 401
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return jsonify({
            'success': False,
            'message': 'Error al procesar la solicitud. Por favor, intenta nuevamente.'
        }), 500

@app.route('/api/register', methods=['POST'])
def api_register():
    """Endpoint para procesar el registro de nuevos usuarios"""
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    company = data.get('company', '')
    
    # Validaciones básicas
    if not all([name, email, password]):
        return jsonify({
            'success': False,
            'message': 'Por favor, completa todos los campos obligatorios.'
        }), 400
    
    # Verificar si el email ya está registrado
    conn = sqlite3.connect('lead_assistant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({
            'success': False,
            'message': 'Este correo electrónico ya está registrado.'
        }), 409
    
    # Crear nuevo usuario
    try:
        password_hash = generate_password_hash(password)
        created_at = datetime.now().isoformat()
        
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, company, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, email, password_hash, company, created_at)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Cuenta creada exitosamente'
        })
    except Exception as e:
        conn.close()
        print(f"Error al registrar usuario: {e}")
        return jsonify({
            'success': False,
            'message': 'Error al crear la cuenta. Por favor, intenta nuevamente.'
        }), 500

@app.route('/api/current_user')
def current_user():
    """Obtiene información del usuario actual"""
    if 'user_id' not in session:
        return jsonify({
            'authenticated': False
        })
    
    return jsonify({
        'authenticated': True,
        'user_id': session['user_id'],
        'name': session['user_name'],
        'email': session['user_email']
    })


@app.route('/api/logout')
def logout():
    """Endpoint para cerrar sesión"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/status')
def status():
    """Ruta para verificar el estado del sistema"""
    return jsonify({
        'data_loaded': data_loaded,
        'llm_available': llm_available,
        'rag_available': rag_available
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para procesar los mensajes del chat (versión no streaming)"""
    data = request.json
    mensaje = data.get('message', '')
    use_streaming = data.get('stream', False)
    
    if use_streaming:
        return streaming_chat()
    
    # Si no hay datos o LLM disponible, devuelve un mensaje genérico
    if not data_loaded or not llm_available:
        return jsonify({
            'response': "Lo siento, el sistema no está completamente disponible en este momento. Por favor verifica que los datos y Ollama estén funcionando correctamente."
        })
    
    # Procesar el mensaje según el tipo
    try:
        if es_saludo(mensaje):
            respuesta = explicar_sistema(mensaje)
        else:
            id_lead = extraer_id_valido(mensaje)
            
            if id_lead:
                # Consulta específica sobre un lead
                filtro = data_df[data_df['id'] == id_lead]
                if not filtro.empty:
                    lead_info = generar_explicacion_textual(filtro.iloc[0])
                    prompt = (
                        f"Información del lead: {lead_info}\n\n"
                        f"Consulta del usuario: {mensaje}\n\n"
                        "Responde a la consulta basándote en la información del lead. "
                        "Asegúrate de dar una respuesta completa y detallada, explicando la puntuación "
                        "y cada uno de los factores que influyeron en ella. "
                        "Incluye recomendaciones específicas basadas en estos factores."
                    )
                    respuesta = llm.invoke(prompt)
                else:
                    respuesta = f"No se encontró información para el ID {id_lead}."
            else:
                # Consulta general para el sistema RAG
                if rag_available:
                    result = qa_chain.invoke(mensaje)
                    # Manejar correctamente la respuesta del sistema RAG
                    if isinstance(result, dict) and 'result' in result:
                        respuesta = result['result']
                    elif isinstance(result, str):
                        respuesta = result
                    else:
                        respuesta = "No he podido encontrar información específica para responder a tu pregunta. ¿Podrías reformularla o ser más específico?"
                else:
                    respuesta = explicar_sistema(mensaje)
    except Exception as e:
        print(f"Error general en chat: {e}")
        respuesta = "Lo siento, ocurrió un error al procesar tu consulta. Por favor, intenta de nuevo."
    
    # Asegurarnos de que la respuesta siempre sea un string
    if not isinstance(respuesta, str):
        respuesta = "No he podido procesar correctamente la respuesta. Por favor, intenta reformular tu pregunta."
    
    return jsonify({
        'response': respuesta
    })

@app.route('/api/streaming-chat', methods=['POST'])
def streaming_chat():
    """Endpoint para procesar los mensajes del chat con streaming mejorado"""
    data = request.json
    mensaje = data.get('message', '')
    
    # Si no hay datos o LLM disponible, devuelve un mensaje genérico
    if not data_loaded or not llm_available:
        def error_stream():
            error_msg = json.dumps({
                'token': "Lo siento, el sistema no está completamente disponible en este momento. Por favor verifica que los datos y Ollama estén funcionando correctamente."
            })
            yield f"data: {error_msg}\n\n"
            yield "data: [DONE]\n\n"
        
        return Response(error_stream(), mimetype='text/event-stream')
    
    # Configurar el streaming LLM con mayor capacidad
    streaming_llm = Ollama(model="gemma3:4b", temperature=0.0, num_predict=2048)
    
    # Procesar el mensaje según el tipo
    try:
        if es_saludo(mensaje):
            stream_generator = explicar_sistema(mensaje, stream=True)
            return Response(stream_generator(), mimetype='text/event-stream')
        else:
            id_lead = extraer_id_valido(mensaje)
            
            if id_lead:
                # Consulta específica sobre un lead
                filtro = data_df[data_df['id'] == id_lead]
                if not filtro.empty:
                    lead_info = generar_explicacion_textual(filtro.iloc[0])
                    prompt = (
                        f"Información del lead: {lead_info}\n\n"
                        f"Consulta del usuario: {mensaje}\n\n"
                        "Responde a la consulta basándote en la información del lead. "
                        "Asegúrate de dar una respuesta completa y detallada, explicando la puntuación "
                        "y cada uno de los factores que influyeron en ella. "
                        "Incluye recomendaciones específicas basadas en estos factores."
                    )
                    
                    def generate_lead_response():
                        try:
                            for chunk in streaming_llm.stream(prompt):
                                yield f"data: {json.dumps({'token': chunk})}\n\n"
                            # Garantizar que se envíe una señal clara de finalización
                            yield "data: {\"token\": \"\\n\"}\n\n"  # Añadir un salto de línea al final
                            yield "data: [DONE]\n\n"
                        except Exception as e:
                            print(f"Error en stream de lead: {e}")
                            yield f"data: {json.dumps({'token': '\\nError en streaming: Intenta recargar la página.'})}\n\n"
                            yield "data: [DONE]\n\n"
                    
                    return Response(generate_lead_response(), mimetype='text/event-stream')
                else:
                    def error_lead_stream():
                        error_msg = json.dumps({
                            'token': f"No se encontró información para el ID {id_lead}."
                        })
                        yield f"data: {error_msg}\n\n"
                        yield "data: [DONE]\n\n"
                    
                    return Response(error_lead_stream(), mimetype='text/event-stream')
            else:
                # Consulta general para el sistema RAG
                if rag_available:
                    # Para RAG, necesitamos crear una consulta que funcione con streaming
                    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
                    relevant_docs = retriever.get_relevant_documents(mensaje)
                    context = "\n\n".join([doc.page_content for doc in relevant_docs])
                    rag_prompt = (
                        f"Contexto: {context}\n\n"
                        f"Consulta del usuario: {mensaje}\n\n"
                        "Responde a la consulta basándote en el contexto proporcionado. "
                        "Asegúrate de dar una respuesta completa y detallada."
                    )
                    
                    def generate_rag_response():
                        try:
                            for chunk in streaming_llm.stream(rag_prompt):
                                yield f"data: {json.dumps({'token': chunk})}\n\n"
                            # Garantizar que se envíe una señal clara de finalización
                            yield "data: {\"token\": \"\\n\"}\n\n"  # Añadir un salto de línea al final
                            yield "data: [DONE]\n\n"
                        except Exception as e:
                            print(f"Error en stream RAG: {e}")
                            yield f"data: {json.dumps({'token': '\\nError en streaming: Intenta recargar la página.'})}\n\n"
                            yield "data: [DONE]\n\n"
                    
                    return Response(generate_rag_response(), mimetype='text/event-stream')
                else:
                    stream_generator = explicar_sistema(mensaje, stream=True)
                    return Response(stream_generator(), mimetype='text/event-stream')
    except Exception as e:
        print(f"Error general en streaming_chat: {e}")
        
        def error_general_stream():
            error_msg = json.dumps({
                'token': "Lo siento, tuve un problema al procesar tu consulta. Por favor, intenta reformularla o pregunta sobre otra cosa."
            })
            yield f"data: {error_msg}\n\n"
            yield "data: [DONE]\n\n"
        
        return Response(error_general_stream(), mimetype='text/event-stream')

@app.route('/api/leads')
def get_leads():
    """Endpoint para obtener la lista de leads disponibles"""
    if not data_loaded:
        return jsonify([])
    
    leads = data_df[['id', 'rating']].to_dict('records')
    return jsonify(leads)

# --- NUEVO ENDPOINT: Agregar nuevo lead ---
@app.route('/api/add_lead', methods=['POST'])
def add_lead():
    """Endpoint para añadir un nuevo lead al sistema"""
    if not data_loaded or not rag_available:
        return jsonify({
            'success': False,
            'message': "El sistema no está completamente disponible. No se puede agregar el lead."
        }), 503
    
    try:
        # Obtener datos del nuevo lead desde la solicitud
        lead_data = request.json
        
        # Validar que el lead tiene los campos requeridos
        required_fields = ['id', 'rating']
        if not all(field in lead_data for field in required_fields):
            return jsonify({
                'success': False,
                'message': f"Faltan campos requeridos. Asegúrate de incluir: {', '.join(required_fields)}"
            }), 400
        
        # Intentar agregar el lead
        success = agregar_nuevo_lead(lead_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': f"Lead con ID {lead_data['id']} agregado correctamente.",
                'id': lead_data['id']
            })
        else:
            return jsonify({
                'success': False,
                'message': f"No se pudo agregar el lead con ID {lead_data['id']}. Puede que ya exista o haya ocurrido un error."
            }), 400
    
    except Exception as e:
        print(f"Error al procesar la solicitud de nuevo lead: {e}")
        return jsonify({
            'success': False,
            'message': f"Error al procesar la solicitud: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Crear la estructura de directorios necesaria
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Inicializar la base de datos
    init_db()
    
    # Crear usuario administrador por defecto
    create_default_admin()
    
    # Iniciar el servidor
    app.run(debug=True, host='0.0.0.0', port=5000)