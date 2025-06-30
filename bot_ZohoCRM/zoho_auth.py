import os
import requests
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_REDIRECT_URI = os.getenv("ZOHO_REDIRECT_URI")
ZOHO_API_BASE = os.getenv("ZOHO_API_BASE")

# Get a fresh access token using the refresh token
def get_access_token():
    url = "https://accounts.zoho.in/oauth/v2/token"
    payload = {
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "redirect_uri": ZOHO_REDIRECT_URI,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]
    else:
        print("❌ Error refreshing access token:", response.text)
        return None
