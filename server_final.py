import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Ton nouveau Webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1464247686936137873/nYqmgjufpGZUvPY7E_4purVnnNT4rx4tkwCGbITiz4MKrqCnYegrorBM1bjBqzLebwyI"

@app.route('/')
def home():
    return "OK", 200

@app.route('/gate', methods=['POST'])
def gate():
    try:
        # On récupère les données brutes si le JSON est mal formé
        data = request.get_json(force=True, silent=True) or {}
        
        user = data.get('x', 'Client')
        type_msg = data.get('y', 'INFO')
        content = data.get('z', 'Commande passée')

        payload = {
            "embeds": [{
                "title": f"🔔 {type_msg}",
                "description": f"**Utilisateur:** {user}\n**Détails:** {content}",
                "color": 5814783
            }]
        }

        # Envoi forcé vers Discord
        requests.post(WEBHOOK_URL, json=payload)
        
        return jsonify({"status": "success"}), 200

    except Exception as e:
        # Même en cas d'erreur, on essaie d'envoyer l'alerte
        requests.post(WEBHOOK_URL, json={"content": f"⚠️ Erreur réception : {str(e)}"})
        return jsonify({"status": "error"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
