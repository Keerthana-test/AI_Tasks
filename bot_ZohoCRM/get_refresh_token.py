import requests

url = "https://accounts.zoho.in/oauth/v2/token"
payload = {
    "grant_type": "authorization_code",
    "client_id": "1000.KCR19ZDJGXOJRN34THKJLT3OLGATEG",
    "client_secret": "a05056bd56820f42d1fc005cabefd3a3a728c3ee92",
    "redirect_uri": "http://localhost:8000/callback",
    "code": "1000.dc0c1210dbe26b5e0e6afef56318d770.f3c1f570d6b2768290e6e4d23ec85f5f"
}

response = requests.post(url, data=payload)
print(response.status_code)
print(response.json())
