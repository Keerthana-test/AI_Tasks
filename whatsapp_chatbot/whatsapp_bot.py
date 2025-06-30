from flask import Flask, request
import requests
import os
import json
from dotenv import load_dotenv
from llm_utils import ask_gemini, ask_ollama

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "testverify123")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID")

user_sessions = {}

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Unauthorized", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("\n[INFO] Received Webhook:")
        print(json.dumps(data, indent=2))

        if data.get("entry"):
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    if messages:
                        for msg in messages:
                            user_id = msg["from"]
                            text = msg["text"]["body"]

                            print(f"[INFO] User ID: {user_id}")
                            print(f"[INFO] Message: {text}")

                            user_data = user_sessions.setdefault(user_id, {"model": None, "history": []})

                            if text.lower() == "/reset":
                                user_sessions[user_id] = {"model": None, "history": []}
                                send_message(user_id, "✅ Chat history reset.\n🤖 Please select a model: Gemini or Ollama")
                                return "ok", 200

                            if not user_data["model"]:
                                if text.lower() in ["gemini", "ollama"]:
                                    user_data["model"] = text.lower()
                                    send_message(user_id, f"✅ Model set to {text.title()}. How can I assist you?")
                                else:
                                    send_message(user_id, "🤖 Please select a model: Gemini or Ollama")
                                return "ok", 200

                            user_data["history"].append({"role": "user", "text": text})

                            # Call the selected model
                            try:
                                if user_data["model"] == "gemini":
                                    reply = ask_gemini(user_data["history"])
                                elif user_data["model"] == "ollama":
                                    reply = ask_ollama(user_data["history"])
                                else:
                                    reply = "🤖 No valid model selected."
                            except Exception as model_error:
                                print(f"[ERROR] Model Error: {model_error}")
                                reply = "⚠️ Failed to generate a reply from the model."

                            user_data["history"].append({"role": "assistant", "text": reply})
                            print(f"[INFO] Bot Reply: {reply}")
                            send_message(user_id, reply)

        return "ok", 200

    except Exception as e:
        print("[ERROR] INTERNAL SERVER ERROR:", e)
        return "Internal Server Error", 500

def send_message(to, message):
    try:
        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }

        res = requests.post(url, headers=headers, json=payload)
        print("[INFO] Sent message response:", res.status_code, res.text)
    except Exception as e:
        print("[ERROR] Failed to send message:", e)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
