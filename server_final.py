import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURATION AUTOMATIQUE ---
WEBHOOKS = {
    "COMMANDE": "https://discord.com/api/webhooks/1462097772353421537/EtSxGaWGRPbn6wOH_a14if5XWaKD52aovBHJLz1gpxCVGuX4PwwogxlTy2v-Z74pfayR",
    "ALERTE": "https://discord.com/api/webhooks/1462098199576842468/9Ty7sTNkj9SJLuyvl71sSKY3_IajGgFtL5QftLqKTGO2TfdyMQyCKGgcEXhk3M74vawp",
    "LOG": "https://discord.com/api/webhooks/1462099070356164469/XFaaqy3Q3V-nevi1scEHIW7a1z1E-09uq5t6WLjXxPY61h6VtEvl3b-WWe_yX4Z8PAJE"
}

SECRET_KEY = "ESCANOR_2024" # Ton nouveau code secret unique

@app.route('/')
def home():
    return "Système Escanor : Opérationnel", 200

@app.route('/gate', methods=['POST'])
def gate():
    auth_key = request.headers.get('X-Escanor-Auth')
    if auth_key != SECRET_KEY:
        return "Erreur d'authentification", 403

    try:
        data = request.get_json()
        user = data.get('x', 'Inconnu')
        msg_type = data.get('y', 'LOG')
        content = data.get('z', '')

        target_webhook = WEBHOOKS.get(msg_type, WEBHOOKS["LOG"])
        
        message = f"**[{msg_type}]**\n👤 Utilisateur : {user}\n📝 Info : {content}"
        requests.post(target_webhook, json={"content": message})
        
        return jsonify({"status": "envoyé"}), 200
    except:
        return jsonify({"status": "erreur"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
