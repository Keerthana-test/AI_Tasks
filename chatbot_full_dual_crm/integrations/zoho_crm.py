import requests

def send_lead_to_zoho(lead_data):
    # Replace with your real Zoho access token
    access_token = "1000.55ff67bc3fe16d63bd2646744f70ff88.582b553d7545218c7a03f66c29cf4c18"
    url = "https://www.zohoapis.in/crm/v2/Leads"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "data": [
            {
                "Last_Name": lead_data["name"],
                "Email": lead_data["email"],
                "Phone": lead_data["phone"],
                "Company": "Chatbot Lead"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
