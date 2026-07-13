import os
import requests
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Environment Variables
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "kvmpbot2516")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_message):
    try:
        if not GEMINI_API_KEY:
            return "ക്ഷമിക്കണം, എനിക്ക് ഇപ്പോൾ മറുപടി നൽകാൻ സാധിക്കുന്നില്ല. എപിഐ കീ സെറ്റ് ചെയ്തിട്ടില്ല."
            
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_message)
        
        # പുതിയ അപ്ഡേറ്റ് പ്രകാരമുള്ള ലളിതമായ കോഡ്
        if response and response.text:
            return response.text
        else:
            return "ക്ഷമിക്കണം, എനിക്ക് ഇപ്പോൾ മറുപടി നൽകാൻ സാധിക്കുന്നില്ല. ദയവായി അല്പം കഴിഞ്ഞ് ശ്രമിക്കൂ."
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "ക്ഷമിക്കണം, എനിക്ക് ഇപ്പോൾ മറുപടി നൽകാൻ സാധിക്കുന്നില്ല. ദയവായി അല്പം കഴിഞ്ഞ് ശ്രമിക്കൂ."

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
        else:
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
                        # ജെമിനിയിൽ നിന്ന് മറുപടി വാങ്ങുന്നു
                        bot_response = get_gemini_response(message_text)
                        # ഫേസ്ബുക്കിലേക്ക് മറുപടി അയക്കുന്നു
                        send_facebook_message(sender_id, bot_response)
    return "EVENT_RECEIVED", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot Server is Running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
