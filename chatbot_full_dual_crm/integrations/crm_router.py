import json
from integrations.zoho_crm import send_lead_to_zoho
from integrations.hubspot_crm import send_lead_to_hubspot

def send_lead_to_crm(lead_data):
    with open("config/crm_config.json") as f:
        config = json.load(f)

    responses = {}

    for crm in config.get("active_crms", []):
        if crm == "zoho":
            responses["zoho"] = send_lead_to_zoho(lead_data)
        elif crm == "hubspot":
            responses["hubspot"] = send_lead_to_hubspot(lead_data)

    return responses
