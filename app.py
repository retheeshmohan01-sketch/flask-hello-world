import os
import requests
from flask import Flask, request

app = Flask(__name__)

# --- നീ ഇപ്പോൾ തന്ന പുതിയ ഫേസ്ബുക്ക് ടോക്കൺ ഞാൻ ഇവിടെ ചേർത്തിട്ടുണ്ട് ---
PAGE_ACCESS_TOKEN = "EAAdLi3MAHMYBRyBAfliNnKD93fdU6gRaGhfGnHmeqZAj4wHSce8LYlVz5iru5vHotrEXIZA8O25WADxsfPA7C0Q185XK1cy3ZA89vrYoh3snXfdKQgBzlVZBUCGafA1ccZC8cEBiREZAx5FZA1YdnQ0BTjooZA0Pxw3EzfpQ7s63bcoJhlZCmsSMIsVmbZCviaE9YYpclyZCsUcqwbjZBAL27HcSHflu6gZDZD"

# --- നീ നേരത്തെ തന്ന Gemini API Key ഞാൻ ഇവിടെ ചേർത്തിട്ടുണ്ട് ---
GEMINI_API_KEY = "AQ.Ab8RN6Kl-dkDKguTTmwrvK5bvRF2a99Eh5rUPi_rlfCbaOWHNQ" 

def get_gemini_response(user_message):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        system_instruction = "നീ Malayali360 പേജിന്റെ ഒരു AI അസിസ്റ്റന്റ് ആണ്. ആളുകൾ ചോദിക്കുന്ന ചോദ്യങ്ങൾക്ക് വളരെ ലളിതമായും സൗഹൃദപരമായും മലയാളത്തിൽ മാത്രം മറുപടി നൽകുക."
        
        payload = {
            "contents": [{"parts": [{"text": user_message}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]}
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        bot_reply = response_data['candidates'][0]['content']['parts'][0]['text']
        return bot_reply
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "ക്ഷമിക്കണം, എനിക്ക് ഇപ്പോൾ മറുപടി നൽകാൻ സാധിക്കുന്നില്ല. ദയവായി അല്പം കഴിഞ്ഞ് ശ്രമിക്കൂ."

# ഫേസ്ബുക്ക് വെബ്ഹൂക്ക് കണക്ഷൻ സ്വീകരിക്കാനുള്ള റൂട്ടുകൾ
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    challenge = request.args.get("hub.challenge")
    if challenge:
        return challenge, 200
    return "Bot is Running Live!", 200

@app.route('/webhook', methods=['POST'])
def fb_webhook():
    data = request.get_json()
    if data and data.get('object') == 'page':
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text', '')

                    if message_text:
                        ai_reply = get_gemini_response(message_text)
                        send_message(sender_id, ai_reply)
    return "Message Processed", 200

def send_message(recipient_id, message_text):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post("https://graph.facebook.com/v12.0/me/messages", params=params, headers=headers, json=data)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
