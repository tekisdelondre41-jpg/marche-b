import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# METHODE RADICALE : Webhook injecté directement
WEBHOOK_URL = "https://discord.com/api/webhooks/1462097772353421537/EtSxGaWGRPbn6wOH_a14if5XWaKD52aovBHJLz1gpxCVGuX4PwwogxITy2v-Z74pfayR"

SECRET_KEY = os.environ.get('X-Escanor-Auth')

@app.route('/')
def home():
    return "Serveur Force Active", 200

@app.route('/gate', methods=['POST'])
def gate():
    auth_key = request.headers.get('X-Escanor-Auth')
    
    if not auth_key or auth_key != SECRET_KEY:
        return "Auth Fail", 401

    try:
        data = request.get_json(force=True)
        user = data.get('x', 'Anonyme')
        content = data.get('z', 'Pas de contenu')

        # Format du message simplifié pour le test
        payload = {
            "content": f"🚀 **TEST RADICAL RÉUSSI** 🚀\n👤 Client : {user}\n📦 Article : {content}"
        }

        # Envoi direct
        response = requests.post(WEBHOOK_URL, json=payload)
        
        return jsonify({"status": "sent", "discord_code": response.status_code}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
