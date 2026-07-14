import os
import requests
from flask import Flask, request

app = Flask(__name__)

FACEBOOK_ACCESS_TOKEN = "EAAdLi3MAHMYByBAFliNnKD93fdU6gRaGhfGnHmeqZAj4wHSce8LYlVz5in"
VERIFY_TOKEN = "kvmpbot2516"
GEMINI_API_KEY = "AQ.Ab8RN6lkz8pUcfgwwlfNAT7L19v4eQeVvVfSgWCaHL1mWa1euw"

def get_gemini_response(user_message):
    try:
        # പുതിയ ഗൂഗിൾ എപിഐ എൻഡ്പോയിന്റ് നേരിട്ട് ഉപയോഗിക്കുന്നു
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": user_message}]
            }]
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        
        if response.status_code == 200 and 'candidates' in res_data:
            return res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Gemini API Error Response: {res_data}")
            return "ക്ഷമിക്കണം, എനിക്ക് ഇപ്പോൾ മറുപടി നൽകാൻ സാധിക്കുന്നില്ല."
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "ക്ഷമിക്കണം, എനിക്ക് ഇപ്പോൾ മറുപടി നൽകാൻ സാധിക്കുന്നില്ല."

def send_facebook_message(recipient_id, text_message):
    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={FACEBOOK_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text_message}
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"FB Send Status: {response.status_code}")
    except Exception as e:
        print(f"FB Send Error: {e}")

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Verification token mismatch", 403
    return "Hello World", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data and data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text", "")
                    if message_text:
                        bot_response = get_gemini_response(message_text)
                        send_facebook_message(sender_id, bot_response)
    return "EVENT_RECEIVED", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot Server is Running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
