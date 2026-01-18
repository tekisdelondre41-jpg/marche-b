from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("ESCANOR_KEY", "TON_CODE_SECRET")
WEBHOOK_BOUTIQUE = os.getenv("WEBHOOK_BOUTIQUE")
WEBHOOK_SPECIAL = os.getenv("WEBHOOK_SPECIAL")
WEBHOOK_LOGS = os.getenv("WEBHOOK_LOGS")

messages_fantomes = []

@app.route('/')
def home():
    return "🛡️ Escanor System Online"

@app.route('/gate', methods=['GET', 'POST'])
def gate():
    try:
        if request.method == 'GET':
            return "Sneakers Limited,150€,https://via.placeholder.com/150\n", 200

        client_key = request.headers.get("X-Escanor-Auth")
        if client_key != API_KEY:
            return "Forbidden", 403

        data = request.get_json()
        if not data:
            return "Bad Request", 400

        type_msg = data.get("type")
        user = str(data.get("user", "Anonyme"))[:30]
        content = str(data.get("content", ""))[:1000]

        payload = {"content": f"**[{type_msg.upper()}]** | {user}: {content}"}
        
        target = WEBHOOK_LOGS
        if type_msg == "achat": target = WEBHOOK_BOUTIQUE
        elif type_msg == "special": target = WEBHOOK_SPECIAL
        
        if target:
            requests.post(target, json=payload, timeout=5)

        if type_msg == "chat":
            messages_fantomes.append({"u": user, "m": content})
            if len(messages_fantomes) > 15:
                messages_fantomes.pop(0)

        return jsonify({"status": "ok", "chat": messages_fantomes}), 200

    except:
        return "Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
