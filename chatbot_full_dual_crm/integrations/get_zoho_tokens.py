import requests

data = {
    "grant_type": "authorization_code",
    "client_id": "1000.3VXOY3OVDDYCORPRY6SM6R4ILG9LAW",
    "client_secret": "36dff82202f4cea70e80bf448e1a3960ae6071e0fe",
    "redirect_uri": "http://localhost:8000/callback",
    "code": "1000.21d3a345f7eb1787256e5e50a8188ec4.26091203e633f29dbe242f8cd58e6953"
}

res = requests.post("https://accounts.zoho.in/oauth/v2/token", data=data)
print(res.json())
