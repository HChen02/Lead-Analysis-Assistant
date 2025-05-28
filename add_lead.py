import requests
import sys
import json

def add_new_lead(lead_data):
    url = "http://localhost:5000/api/add_lead"
    response = requests.post(url, json=lead_data)
    return response.json(), response.status_code

if __name__ == "__main__":
    # Ejemplo de datos de lead
    lead = {"categoria_producto1": 0.0007574827075586, 
            "country": -0.0008533623270826, 
            "dtime_created_aircall_last_call_at": 0.0005207786473329, 
            "dtime_created_first_conversion_date": 0.000695517725641, 
            "dtime_created_first_deal_created_date": -0.0002288581864559, 
            "dtime_created_hs_analytics_first_timestamp": -4.361740876144323e-05, 
            "dtime_created_hs_analytics_first_visit_timestamp": 0.0003166922439898, 
            "dtime_created_hs_analytics_last_visit_timestamp": 0.0001695551051913, 
            "dtime_created_hs_email_first_click_date": -0.0074601555587044, 
            "dtime_created_hs_email_first_open_date": -0.0003014760736065, 
            "dtime_created_hs_email_first_send_date": 0.0033051582223076, 
            "dtime_created_hs_first_outreach_date": 0.0003803539911556, 
            "dtime_created_hs_latest_source_timestamp": 0.0002711732745713, 
            "dtime_created_hs_v2_date_exited_lead": 0.0007199277560478, 
            "dtime_created_hs_v2_date_exited_subscriber": 0.0, 
            "dtime_created_mass_update": -3.903882034743834e-05, 
            "dtime_created_predicted_at": 4.038168117404446e-06, 
            "dtime_created_recent_conversion_date": 0.0, 
            "dtime_from_hs_email_first_send_date_to_hs_email_first_click_date": -0.0005336776504797, 
            "dtime_from_hs_email_first_send_date_to_hs_email_first_open_date": 0.0021229296268332, 
            "dtime_from_hs_email_last_send_date_to_hs_email_last_click_date": 0.0, 
            "dtime_from_hs_email_last_send_date_to_hs_email_last_open_date": 0.0, 
            "dtime_predicted_first_conversion_date": 0.0, 
            "dtime_predicted_hs_analytics_first_timestamp": -0.0013637481370824, 
            "dtime_predicted_hs_analytics_first_visit_timestamp": -4.701803263742453e-06, 
            "dtime_predicted_hs_last_sales_activity_date": 0.0002243752067442, 
            "dtime_predicted_hs_last_sales_activity_timestamp": -4.406861747459804e-05, 
            "dtime_predicted_hs_latest_meeting_activity": -0.0007359134470849, 
            "dtime_predicted_hs_lifecyclestage_opportunity_date": 0.0026296839791272, 
            "dtime_predicted_hs_sa_first_engagement_date": -0.0001088338951619, 
            "dtime_predicted_hs_sales_email_last_clicked": -0.0054510281709372, 
            "dtime_predicted_hs_sales_email_last_replied": -0.0013326460750734, 
            "dtime_predicted_hs_v2_date_entered_opportunity": 0.0002067968967215, 
            "dtime_predicted_hubspot_owner_assigneddate": -0.0002667983292485, 
            "dtime_predicted_lead_history_captacion_modified": -5.597580631729215e-05, 
            "dtime_predicted_lead_history_explotacion_modified": -0.0016460396464875, 
            "dtime_predicted_notes_last_contacted": -0.0002131717899465, 
            "dtime_predicted_notes_last_updated": 0.0002575649424882, 
            "dtime_predicted_recent_conversion_date": -0.0003291770201758, 
            "email_domain": -0.0007968255413288, 
            "producto_sql": -0.0022138820939774, 
            "first_conversion_event_name": 0.0004030011230982, 
            "from_hs_analytics_first_timestamp_to_hs_analytics_last_timestamp": 0.0061882370479482, 
            "from_hs_analytics_first_visit_timestamp_to_hs_analytics_last_visit_timestamp": -0.0005342445955223, 
            "hs_all_contact_vids_count": 0.0, "hs_analytics_average_page_views": -3.5866430456128924e-05, 
            "hs_analytics_first_referrer.domain": 0.000202523463037, 
            "hs_analytics_first_referrer.path": -6.362677673071931e-05, 
            "hs_analytics_first_referrer.tld": 0.0004950187093345, 
            "hs_analytics_first_url.domain": 0.0001394999067997, 
            "hs_analytics_first_url.path": -0.0005381245327589, 
            "hs_analytics_first_url.tld": 0.0, 
            "hs_analytics_last_referrer.domain": 0.0, 
            "hs_analytics_last_referrer.path": -0.0016520205851217, 
            "hs_analytics_last_referrer.tld": 0.0001438556165279, 
            "hs_analytics_source": 0.0003722426884147, 
            "hs_analytics_source_data_1": -0.0002098244873923, 
            "hs_analytics_source_data_2": 0.0002534884020375, 
            "hs_calculated_form_submissions_count": -2.736678754445213e-05, 
            "hs_ip_timezone0": -0.0001783320620112, 
            "hs_ip_timezone1": -0.0006034074029594, 
            "hs_language": -5.487273107670779e-05, 
            "hs_latest_source": 0.002335230782822, 
            "hs_latest_source_data_1": 5.5210569019739694e-05, 
            "hs_latest_source_data_2": -0.0002972083282171, 
            "ip_country": -0.0010228442130998, 
            "ip_state_code": -2.772555065651901e-05, 
            "jobtitle": -0.0002657290965726, 
            "categoria_producto2": 0.0003944204027842, 
            "codigo_sql": -0.0001721245647058, 
            "level_of_studies": -0.0086850401343932, 
            "message_len": -0.0006402944957759, 
            "num_leads": 1.1745352627865564e-05, 
            "recent_conversion_event_name": 0.0001006913794359, 
            "source_sql": -0.0014667220388461, 
            "utm_campaign": -0.0042243402656943, 
            "utm_content": -0.005154477275549, 
            "utm_source": -0.0005336680096418, 
            "shap_base_value": 0.0274861080781556, 
            "score_x": 0.0007524452521465, 
            "id": "8f069d1b3b73__20240101001842", 
            "user_id": "8f069d1b3b73", 
            "prediction_date": "2024-01-01 00:18:42+00:00", 
            "score_y": 0.00075244525, 
            "rating": "D"
    }
    
    
    # También puedes cargar datos desde un archivo JSON
    # with open('nuevo_lead.json', 'r') as f:
    #     lead = json.load(f)
    
    result, status_code = add_new_lead(lead)
    print(f"Estado: {status_code}")
    print(json.dumps(result, indent=2))



