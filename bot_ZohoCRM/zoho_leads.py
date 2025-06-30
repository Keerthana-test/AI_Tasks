import requests
from zoho_auth import get_access_token
import os
from dotenv import load_dotenv

load_dotenv()
ZOHO_API_BASE = os.getenv("ZOHO_API_BASE")  # e.g., https://www.zohoapis.com

# 🔍 Search lead by phone number
def search_lead_by_phone(phone_number):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    url = f"{ZOHO_API_BASE}/crm/v2/Leads/search?phone={phone_number}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            return data["data"][0]  # Found lead
        else:
            return None  # No lead found
    else:
        print("❌ Error searching lead:", response.text)
        return None

# ➕ Create a new lead
def create_lead(name, email, phone_number):
    access_token = get_access_token()
    if not access_token:
        print("❌ No access token retrieved.")
        return None

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    url = f"{ZOHO_API_BASE}/crm/v2/Leads"
    payload = {
        "data": [
            {
                "Last_Name": name,
                "Email": email,
                "Phone": phone_number,
                "Lead_Source": "Chatbot"
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    print("📤 Sent data:", payload)
    print("📥 Zoho Response Code:", response.status_code)
    print("📥 Zoho Response Text:", response.text)

    if response.status_code == 201:
        return response.json()["data"][0]
    else:
        return None

