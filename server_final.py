import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

WEBHOOK_URL = "https://discord.com/api/webhooks/1461778274698133826/yddifNr8KNH3CTB3TlrcpJwgwOD5U3TfkPcODzvaTQrT4_yhFThulcWfTVRt6PwCtmLo"

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
        content = data.get('z', 'Pas de contenu')

        payload = {
            "content": f"🛒 **NOUVELLE COMMANDE** 🛒\n👤 Client : {user}\n📦 Détails : {content}"
        }

        requests.post(WEBHOOK_URL, json=payload)
        
        return jsonify({"status": "sent"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
