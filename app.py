from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def fb_webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == 'kvmpbot2516':
            return challenge, 200
        return 'Invalid verification token', 403
        
    return 'Bot Running', 200
