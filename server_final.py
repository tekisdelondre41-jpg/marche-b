import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Ton nouveau Webhook Discord (celui qui finit par ...bwyI)
WEBHOOK_URL = "https://discord.com/api/webhooks/1464247686936137873/nYqmgjufpGZUvPY7E_4purVnnNT4rx4tkwCGbITiz4MKrqCnYegrorBM1bjBqzLebwyI"

@app.route('/')
def home():
    return "SERVEUR OPERATIONNEL", 200

@app.route('/gate', methods=['POST'])
def gate():
    try:
        # On force la lecture même si le format est brut
        raw_data = request.data.decode('utf-8')
        print(f"Données reçues : {raw_data}") # Apparaîtra dans tes logs Render

        data = request.get_json(force=True, silent=True) or {}
        
        user_num = data.get('x', 'Inconnu')
        item = data.get('z', 'Aucun article sélectionné')

        payload = {
            "username": "Ma Boutique Tekis",
            "embeds": [{
                "title": "🛒 Nouvelle Commande !",
                "color": 15418782,
                "fields": [
                    {"name": "📞 Numéro Client", "value": str(user_num), "inline": True},
                    {"name": "📦 Article", "value": str(item), "inline": True}
                ],
                "footer": {"text": "Validation via App"}
            }]
        }

        requests.post(WEBHOOK_URL, json=payload)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
