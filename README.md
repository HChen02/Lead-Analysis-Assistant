# Lead Analysis Assistant [ENGLISH]

![Lead Analysis Assistant Logo](https://img.shields.io/badge/Lead%20Analysis-Assistant-4F46E5)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Description

Lead Analysis Assistant is a web application that uses artificial intelligence to analyze and classify leads (potential business contacts), providing detailed insights into their purchase potential. The application combines machine learning techniques with natural language processing to offer clear explanations about the factors that influence each lead's score.

The system includes:
- Modern and responsive user interface
- User authentication system
- Interactive dashboard to visualize and query leads
- Integrated chatbot with RAG (Retrieval Augmented Generation) capabilities
- API for integration with other systems

## Screenshots

### Login Screen
![Login Screen](https://private-us-east-1.manuscdn.com/sessionFile/zyREOBFokVl9mOXY0yJKau/sandbox/loSkDYSJfLpW1jAe3rEaod-images_1748440202098_na1fn_L2hvbWUvdWJ1bnR1L2ltYWdlcy9sb2dpbg.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvenlSRU9CRm9rVmw5bU9YWTB5SkthdS9zYW5kYm94L2xvU2tEWVNKZkxwVzFqQWUzckVhb2QtaW1hZ2VzXzE3NDg0NDAyMDIwOThfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwybHRZV2RsY3k5c2IyZHBiZy5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NjcyMjU2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=Wst88YwH2lMRW29zHtCU2EoJu73j7ET1jRmWzqYhPamSMs9Cssw-J4FfWB0J~lLzlb78IDyUYorNuwENgL~ogikiWunyJQxlvt6Fz7py8dgDb9vtMe5QC9hvobBRAdYdRfyT3v3HImdslyyDaLw64s58UqqqDcI4H7LEfhCGQh07jISDAmTyD1dMEyMlmTOuXuGPu6PYif1qIc1zg2NtM-ZzkvE0i3mwofCYMwA1TX416cvP9EJEC0k3Jk0bwoXIA7ZstepizdeFjaw5GZxQFCA2yephuTQasWo-9KB~-MpzCfiVPQUVZy5fABBzY3trhWoiqJcyeag17EYkuuNVEQ__)

### Main Dashboard
![Main Dashboard](https://private-us-east-1.manuscdn.com/sessionFile/zyREOBFokVl9mOXY0yJKau/sandbox/loSkDYSJfLpW1jAe3rEaod-images_1748440202099_na1fn_L2hvbWUvdWJ1bnR1L2ltYWdlcy9kYXNoYm9hcmQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvenlSRU9CRm9rVmw5bU9YWTB5SkthdS9zYW5kYm94L2xvU2tEWVNKZkxwVzFqQWUzckVhb2QtaW1hZ2VzXzE3NDg0NDAyMDIwOTlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwybHRZV2RsY3k5a1lYTm9ZbTloY21RLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=two1Ww21NUEnw9PbDuD~fgufrA1vo~jFj-H5ntkVqvw4dMiFMmhwYKcKPvWcamT72jK5KcW97XMxI12KH6ML3K0Hoa1p0SrrK5SevQnFv3ODHgZa4mVPJcUyrqt8ZOIDp7NRL-qx7SjJkwtL4y1oBOHS4oe3DU78KBBlqKA-AISv4O8IK6HrvER~fQ9016EMhf~emnvfO54dF65I2erd9OTsDSoKgMVbbhX-c4EvPYyZsklAP3vEMocUTStGDUrhiQn1THKVK6EX1KQctYluK6P5Je~ww2Zha5nfCRf6Lbr0HJu8F6mMNsFN1wNUmJmWAugNLFc07LCElnc0V9tUzg__)

## Key Features

- **Lead Analysis**: Automatic classification of leads according to their purchase potential (A, B, C, D)
- **Natural Language Explanations**: Interpretation of the factors that influence each score
- **User Authentication**: Complete registration and login system
- **Intelligent Chatbot**: AI-based assistant for queries about specific leads or general trends
- **Responsive Interface**: Design adaptable to mobile and desktop devices
- **Integration API**: Endpoints to add new leads and query information

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **AI Models**:
  - Ollama (Local LLM)
  - FAISS (Vector store)
  - LangChain (Framework for AI applications)
  - HuggingFace Embeddings

## Prerequisites

- Python 3.6+
- Ollama installed locally (for LLM functionalities)
- Modern web browser

## Installation

1. Clone this repository:
```bash
git clone https://github.com/HChen02/Lead-Analysis-Assistant.git
cd lead-analysis-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure you have Ollama installed and the gemma3:4b model available:
```bash
# Install Ollama following the instructions at https://ollama.ai/
ollama pull gemma3:4b
```

5. Prepare the data files (optional, the application can work in demo mode without them):
   - `shap_values.csv`: SHAP values for each lead
   - `prediction.csv`: Predictions and classifications for each lead
   - `description_crm_data.csv`: Descriptions of CRM variables

6. Start the application:
```bash
python app.py
```

7. Access the application in your browser:
```
http://localhost:5000
```

## File Structure

```
lead-analysis-assistant/
├── app.py                  # Main Flask application
├── add_lead.py             # Script to add new leads
├── templates/
│   ├── login.html          # Login page
│   └── dashboard.html      # Main dashboard
├── static/
│   ├── css/                # CSS files
│   ├── js/                 # JavaScript files
│   └── favicon.ico         # Favicon
├── shap_values.csv         # SHAP values for each lead
├── prediction.csv          # Predictions and classifications
├── description_crm_data.csv # Variable descriptions
├── faiss_index/            # FAISS vector index
├── lead_assistant.db       # SQLite database
└── requirements.txt        # Project dependencies
```

## Usage

### Accessing the Application

1. Start the application with `python app.py`
2. Access `http://localhost:5000` in your browser
3. Log in with the default credentials:
   - Email: admin@leadanalysis.com
   - Password: admin123

### Querying Leads

1. Browse the list of leads in the side panel
2. Select a lead to view its details
3. Use the chatbot to ask specific questions about the selected lead

### General Queries

You can ask general questions to the chatbot about:
- Factors that influence scores
- Trends in the data
- Recommendations to improve lead quality

### Adding New Leads

You can add new leads using the `add_lead.py` script:

```bash
python add_lead.py
```

Or via a POST request to the API:

```bash
curl -X POST -H "Content-Type: application/json" -d @new_lead.json http://localhost:5000/api/add_lead
```

## API Reference

### Available Endpoints

#### Authentication

- `POST /api/login`: Log in
- `POST /api/register`: Register new user
- `GET /api/logout`: Log out
- `GET /api/current_user`: Get current user information

#### Leads and Chat

- `POST /api/chat`: Send message to chatbot
- `GET /api/chat/stream`: Streaming version of the chatbot
- `POST /api/add_lead`: Add new lead
- `GET /api/status`: Check system status

## Development

### Main Dependencies

The main dependencies of the project are:

```
flask
pandas
langchain
langchain_community
langchain_huggingface
faiss-cpu
ollama
sqlite3
werkzeug
```

### Development Configuration

1. Clone the repository
2. Install development dependencies
3. Run the application in debug mode:
```bash
FLASK_ENV=development python app.py
```

## Contributions

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Name - Hao Chen - hc754491@gmail.com

Project Link: [https://github.com/your-username/lead-analysis-assistant](https://github.com/HChen02/Lead-Analysis-Assistant)

## Acknowledgments

- [Ollama](https://ollama.ai/) for providing local language models
- [LangChain](https://www.langchain.com/) for the AI application framework
- [FAISS](https://github.com/facebookresearch/faiss) for the similarity search library
- [ByRATINGS](https://byratings.com/es/) for the data of the project


# Lead Analysis Assistant [SPANISH]

![Lead Analysis Assistant Logo](https://img.shields.io/badge/Lead%20Analysis-Assistant-4F46E5)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Descripción

Lead Analysis Assistant es una aplicación web que utiliza inteligencia artificial para analizar y clasificar leads (contactos comerciales potenciales), proporcionando insights detallados sobre su potencial de compra. La aplicación combina técnicas de machine learning con procesamiento de lenguaje natural para ofrecer explicaciones claras sobre los factores que influyen en la puntuación de cada lead.

El sistema incluye:
- Interfaz de usuario moderna y responsiva
- Sistema de autenticación de usuarios
- Dashboard interactivo para visualizar y consultar leads
- Chatbot integrado con capacidades de RAG (Retrieval Augmented Generation)
- API para integración con otros sistemas

## Capturas de pantalla

### Pantalla de inicio de sesión
![Pantalla de inicio de sesión](https://private-us-east-1.manuscdn.com/sessionFile/zyREOBFokVl9mOXY0yJKau/sandbox/WPqOMrLQZ20kFAOfNxhwSg-images_1748438560805_na1fn_L2hvbWUvdWJ1bnR1L2ltYWdlcy9sb2dpbg.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvenlSRU9CRm9rVmw5bU9YWTB5SkthdS9zYW5kYm94L1dQcU9NckxRWjIwa0ZBT2ZOeGh3U2ctaW1hZ2VzXzE3NDg0Mzg1NjA4MDVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwybHRZV2RsY3k5c2IyZHBiZy5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NjcyMjU2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=ZMC-Om4sL1bzUXr0qhPzZeLN-nf4qKYEpUoDxwimayx~B6HgCIhYWfyxh6ulqfKQBR9lksMKq-eL1NvaNE7pQr3DjPaaCW~6mKn2mf3UZdqUzGJsOOvK2BuHvSpwRFzMHCFkCuEpunwc-CytaypZj-USbxtXHMMdJZ45iD22Jkut7JDqEpxwdEPDOg~nh8CnEVa1KYo8mi2aRyZlQg1MvSaoMPuPHLd9TlFhCeu0QV9NlezUXANU3PBVAr3og-5QFrj8XrCxgcFOl8BGazY~Mqra-wLTBEYCBZ~KdlTI6WGn20Zcq3uxynltTOtcg58~hIrsVm8f8L5E5hRJeOd0AQ__)

### Dashboard principal
![Dashboard principal](https://private-us-east-1.manuscdn.com/sessionFile/zyREOBFokVl9mOXY0yJKau/sandbox/WPqOMrLQZ20kFAOfNxhwSg-images_1748438560806_na1fn_L2hvbWUvdWJ1bnR1L2ltYWdlcy9kYXNoYm9hcmQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvenlSRU9CRm9rVmw5bU9YWTB5SkthdS9zYW5kYm94L1dQcU9NckxRWjIwa0ZBT2ZOeGh3U2ctaW1hZ2VzXzE3NDg0Mzg1NjA4MDZfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwybHRZV2RsY3k5a1lYTm9ZbTloY21RLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=YFFy8g20jYQfW6Dlr32ICuOfordbRIynMRYGEolLA4QNP~Bjg-pK08jnFHhMNmEAgdJyT7loKJcZll4uD-4VWLKJrOMPgTrS7xozDqROj7bs6mWJitm7lO4Av-i9W7DY6JHCAOCwlzJYOQktk~AJmZthQZDitNTAYNDD8j332LrENjNf7LI6CjZ2V9iga-341ab2sua5SCtIpCW35hF7vhzuaR5fAvAaBwGlTXFzPaEXAPgzP6-m2lb0jEguTW9B-4rMOWPQ845k3Vfz3gE6KwPSfzwe4I~Zu16njjrDinZH78jGjtR9oW2VYiJVP0y6MILbxAXbvR9cFOd5WmgxZQ__)

## Características principales

- **Análisis de leads**: Clasificación automática de leads según su potencial de compra (A, B, C, D)
- **Explicaciones en lenguaje natural**: Interpretación de los factores que influyen en cada puntuación
- **Autenticación de usuarios**: Sistema completo de registro e inicio de sesión
- **Chatbot inteligente**: Asistente basado en IA para consultas sobre leads específicos o tendencias generales
- **Interfaz responsiva**: Diseño adaptable a dispositivos móviles y de escritorio
- **API para integración**: Endpoints para agregar nuevos leads y consultar información

## Tecnologías utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Base de datos**: SQLite
- **Modelos de IA**:
  - Ollama (LLM local)
  - FAISS (Vector store)
  - LangChain (Framework para aplicaciones de IA)
  - HuggingFace Embeddings

## Requisitos previos

- Python 3.6+
- Ollama instalado localmente (para funcionalidades de LLM)
- Navegador web moderno

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/HChen02/Lead-Analysis-Assistant.git

cd lead-analysis-assistant
```

2. Crea y activa un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Asegúrate de tener Ollama instalado y el modelo gemma3:4b disponible:
```bash
# Instala Ollama según las instrucciones en https://ollama.ai/
ollama pull gemma3:4b
```

5. Prepara los archivos de datos (opcional, la aplicación puede funcionar en modo demo sin ellos):
   - `shap_values.csv`: Valores SHAP para cada lead
   - `prediction.csv`: Predicciones y clasificaciones para cada lead
   - `description_crm_data.csv`: Descripciones de las variables del CRM

6. Inicia la aplicación:
```bash
python app.py
```

7. Accede a la aplicación en tu navegador:
```
http://localhost:5000
```

## Estructura de archivos

```
lead-analysis-assistant/
├── app.py                  # Aplicación principal Flask
├── add_lead.py             # Script para agregar nuevos leads
├── templates/
│   ├── login.html          # Página de inicio de sesión
│   └── dashboard.html      # Dashboard principal
├── static/
│   ├── css/                # Archivos CSS
│   ├── js/                 # Archivos JavaScript
│   └── favicon.ico         # Favicon
├── shap_values.csv         # Valores SHAP para cada lead
├── prediction.csv          # Predicciones y clasificaciones
├── description_crm_data.csv # Descripciones de variables
├── faiss_index/            # Índice vectorial FAISS
├── lead_assistant.db       # Base de datos SQLite
└── requirements.txt        # Dependencias del proyecto
```

## Uso

### Acceso a la aplicación

1. Inicia la aplicación con `python app.py`
2. Accede a `http://localhost:5000` en tu navegador
3. Inicia sesión con las credenciales predeterminadas:
   - Email: admin@leadanalysis.com
   - Contraseña: admin123

### Consulta de leads

1. Navega por la lista de leads en el panel lateral
2. Selecciona un lead para ver sus detalles
3. Utiliza el chatbot para hacer preguntas específicas sobre el lead seleccionado

### Consultas generales

Puedes hacer preguntas generales al chatbot sobre:
- Factores que influyen en las puntuaciones
- Tendencias en los datos
- Recomendaciones para mejorar la calidad de los leads

### Agregar nuevos leads

Puedes agregar nuevos leads mediante el script `add_lead.py`:

```bash
python add_lead.py
```

O mediante una solicitud POST a la API:

```bash
curl -X POST -H "Content-Type: application/json" -d @nuevo_lead.json http://localhost:5000/api/add_lead
```

## API Reference

### Endpoints disponibles

#### Autenticación

- `POST /api/login`: Iniciar sesión
- `POST /api/register`: Registrar nuevo usuario
- `GET /api/logout`: Cerrar sesión
- `GET /api/current_user`: Obtener información del usuario actual

#### Leads y Chat

- `POST /api/chat`: Enviar mensaje al chatbot
- `GET /api/chat/stream`: Versión streaming del chatbot
- `POST /api/add_lead`: Agregar nuevo lead
- `GET /api/status`: Verificar estado del sistema

## Desarrollo

### Dependencias principales

Las principales dependencias del proyecto son:

```
flask
pandas
langchain
langchain_community
langchain_huggingface
faiss-cpu
ollama
sqlite3
werkzeug
```

### Configuración para desarrollo

1. Clona el repositorio
2. Instala las dependencias de desarrollo
3. Ejecuta la aplicación en modo debug:
```bash
FLASK_ENV=development python app.py
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork el repositorio
2. Crea una rama para tu característica (`git checkout -b feature/amazing-feature`)
3. Realiza tus cambios
4. Commit tus cambios (`git commit -m 'Add some amazing feature'`)
5. Push a la rama (`git push origin feature/amazing-feature`)
6. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Contacto

Nombre - Hao Chen - hc754491@gmail.com

Link del proyecto: [https://github.com/your-username/lead-analysis-assistant](https://github.com/HChen02/Lead-Analysis-Assistant)

## Agradecimientos

- [Ollama](https://ollama.ai/) por proporcionar modelos de lenguaje locales
- [LangChain](https://www.langchain.com/) por el framework para aplicaciones de IA
- [FAISS](https://github.com/facebookresearch/faiss) por la biblioteca de búsqueda de similitud
- [ByRATINGS](https://byratings.com/es/) por data del proyecto
