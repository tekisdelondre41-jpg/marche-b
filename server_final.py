import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Récupération des secrets sur Render
WEBHOOKS = {
    "COMMANDE": os.environ.get('WEBHOOK_BOUTIQUE'),
    "ALERTE": os.environ.get('WEBHOOK_VIP'),
    "SMS": os.environ.get('WEBHOOK_VIP'),
    "LOG": os.environ.get('WEBHOOK_LOGS')
}
SECRET_KEY = os.environ.get('ESCANOR_KEY')

@app.route('/gate', methods=['POST'])
def gate():
    # Vérification de sécurité simple
    if request.headers.get('X-Escanor-Auth') != SECRET_KEY:
        return "Auth Fail", 401

    try:
        # On récupère x, y, z (plus d'erreurs de noms longs)
        data = request.get_json(force=True)
        user = data.get('x', 'Inconnu')
        msg_type = data.get('y', 'LOG')
        content = data.get('z', 'Pas de contenu')

        # Choix du salon Discord
        url = WEBHOOKS.get(msg_type, WEBHOOKS["LOG"])
        
        # Envoi propre vers Discord
        if url:
            payload = {"content": f"**[{msg_type}]**\n👤 {user}\n📝 {content}"}
            requests.post(url, json=payload)
        
        return jsonify({"status": "ok"}), 200
    except:
        return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
