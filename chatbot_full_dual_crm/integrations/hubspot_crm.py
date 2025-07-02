import requests

def send_lead_to_hubspot(lead_data):
    # Replace with your real HubSpot Private App token
    access_token = "your-secret-api-key"
    url = "https://api.hubapi.com/crm/v3/objects/contacts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "properties": {
            "email": lead_data["email"],
            "firstname": lead_data["name"],
            "phone": lead_data["phone"],
            "lifecyclestage": "lead"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
