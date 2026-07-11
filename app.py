from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAdLi3MAHMYBR5PyWho3knsJ52knqZBO99IcYGVa7OT92IvfrESBP2jvLqVs46tnfyE33KSl4keLZCZALeD1AZAiW3w82soqtMLNki5gVMHGV2Qu01eHERFvH8xGoWa9gCoQkO3n3h4icnXd4jiZAnjQ4rWZCbYUjJmyvKFAZBYfiJH46YhEVRV699S8y7m3f9p4qcMn1JxGq2KcAFq8E4v4vyWiAZDZD'

def send_message(sender_id, text):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": text}
    }
    requests.post(url, json=payload)

@app.route('/', methods=['GET', 'POST'])
def fb_webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == 'kvmpbot2516':
            return challenge, 200
        return 'Invalid verification token', 403
        
    elif request.method == 'POST':
        data = request.get_json()
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    if messaging_event.get('message'):
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text', '')
                        
                        # ബോട്ട് തിരിച്ച് അയക്കുന്ന മറുപടി ഇവിടെ സെറ്റ് ചെയ്യുന്നു
                        if message_text:
                            send_message(sender_id, "വാർത്തകൾ | വിശേഷങ്ങൾ | വൈറൽ | അറിവുകൾ | വിനോദം.  അറിയുവാൻ വേണ്ടി Malayali360 പേജിലേക്ക് സ്വാഗതം")
                            
        return 'EVENT_RECEIVED', 200

    return 'Bot Running', 200
