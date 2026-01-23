import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

WEBHOOK_URL = "https://discord.com/api/webhooks/1461778274698133826/yddifNr8KNH3CTB3TlrcpJwgwOD5U3TfkPcODzvaTQrT4_yhFThulcWfTVRt6PwCtmLo"

@app.route('/')
def home():
    return "OK", 200

@app.route('/gate', methods=['POST'])
def gate():
    try:
        data = request.get_json(force=True)
        user = data.get('x', 'Testeur')
        content = data.get('z', 'Test Message')

        payload = {
            "content": f"🚨 **TEST SANS SÉCURITÉ** 🚨\n👤 Client : {user}\n📦 Détails : {content}"
        }

        requests.post(WEBHOOK_URL, json=payload)
        return jsonify({"status": "sent"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
