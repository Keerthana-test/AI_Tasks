# test_access_token.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://accounts.zoho.com/oauth/v2/token"
payload = {
    "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
    "client_id": os.getenv("ZOHO_CLIENT_ID"),
    "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
    "redirect_uri": os.getenv("ZOHO_REDIRECT_URI"),
    "grant_type": "refresh_token"
}

response = requests.post(url, data=payload)
print(response.status_code)
print(response.json())
    