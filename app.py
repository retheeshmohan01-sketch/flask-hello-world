import os
import requests
from flask import Flask, request

app = Flask(__name__)

# --- നിന്റെ ഫേസ്ബുക്ക് ടോക്കൺ ---
PAGE_ACCESS_TOKEN = "EAAdLi3MAHMYBR5PyWho3knsJ52knqZBO99IcYGVa7OT92IvfrESBP2jvLqVs46tnfyE33KSl4keLZCZALeD1AZAiW3w82soqtMLNki5gVMHGV2Qu01eHERFvH8xGoWa9gCoQkO3n3h4icnXd4jiZAnjQ4rWZCbYUjJmyvKFAZBYfiJH46YhEVRV699S8y7m3f9p4qcMn1JxGq2KcAFq8E4v4vyWiAZDZD"

# --- നിന്റെ GEMINI API KEY ---
GEMINI_API_KEY = "AQ.Ab8RN6Jm_ctU5lXNs0yxNYQMjaWXDHcydZpGmQZ_ZigJaPvRsA" 

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

# --- മെയിൻ റൂട്ടിലും വെബ്ഹൂക്ക് സ്വീകരിക്കാൻ മാറ്റം വരുത്തി ---
@app.route('/', methods=['GET'])
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    return request.args.get("hub.challenge", "Bot is Running Live!")

@app.route('/', methods=['POST'])
@app.route('/webhook', methods=['POST'])
def fb_webhook():
    data = request.get_json()
    if data.get('object') == 'page':
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
