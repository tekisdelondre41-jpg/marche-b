import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
MON_EMAIL = "oazizdelondre41@gmail.com"
MON_CODE_GOOGLE = "lnii lglu oysj atuo"

@app.route('/')
def home():
    return "SERVEUR BOUTIQUE ACTIF", 200

@app.route('/gate', methods=['POST'])
def gate():
    try:
        # Récupération des données de ton application (blocs x, y, z)
        data = request.get_json(force=True, silent=True) or {}
        numero_client = data.get('x', 'Inconnu')
        article = data.get('z', 'Aucun article sélectionné')

        # Préparation de l'email
        msg = EmailMessage()
        msg.set_content(f"Nouvelle commande reçue !\n\nNuméro du client : {numero_client}\nArticle : {article}")
        msg['Subject'] = f"🛒 Commande de {numero_client}"
        msg['From'] = MON_EMAIL
        msg['To'] = MON_EMAIL

        # Connexion et envoi sécurisé via Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MON_EMAIL, MON_CODE_GOOGLE)
            smtp.send_message(msg)

        print(f"Commande de {numero_client} envoyée par mail.")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
