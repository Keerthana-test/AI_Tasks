from parsers.lead_parser import parse_lead
from integrations.crm_router import send_lead_to_crm

def handle_user_input(name, email, phone):
    lead_data = parse_lead(name, email, phone)
    crm_result = send_lead_to_crm(lead_data)
    return crm_result
