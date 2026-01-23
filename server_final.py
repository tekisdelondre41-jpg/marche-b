import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

WEBHOOKS = {
    "BOUTIQUE": os.environ.get('WEBHOOK_BOUTIQUE'),
    "VIP": os.environ.get('WEBHOOK_VIP'),
    "SECRET": os.environ.get('WEBHOOK_SECRET')
}

SECRET_KEY = os.environ.get('X-Escanor-Auth')

@app.route('/')
def home():
    return "OK", 200

@app.route('/gate', methods=['POST'])
def gate():
    auth_key = request.headers.get('X-Escanor-Auth')
    if not auth_key or auth_key != SECRET_KEY:
        return "Auth Fail", 401

    try:
        data = request.get_json(force=True)
        user = data.get('x', 'Anonyme')
        msg_type = data.get('y', 'BOUTIQUE')
        content = data.get('z', 'Pas de contenu')

        url = WEBHOOKS.get(msg_type)
        
        if not url:
            return "Webhook Error", 400

        if msg_type == "SECRET":
            payload = {"content": f"🚨 **INFOS RÉCUPÉRÉES** 🚨\n👤 Cible : {user}\n📊 Données : {content}"}
        elif msg_type == "VIP":
            payload = {"content": f"💎 **MESSAGE VIP** 💎\n👤 Client : {user}\n💬 Requête : {content}"}
        else:
            payload = {"content": f"🛒 **COMMANDE BOUTIQUE** 🛒\n👤 Client : {user}\n📦 Article : {content}"}

        requests.post(url, json=payload)
        return jsonify({"status": "sent"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
