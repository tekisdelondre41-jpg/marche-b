from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_BOUTIQUE = "https://discord.com/api/webhooks/1462097772353421537/EtSxGaWGRPbn6wOH_a14if5XWaKD52aovBHJLz1gpxCVGuX4PwwogxITy2v-Z74pfayR"
WEBHOOK_SPECIAL = "https://discord.com/api/webhooks/1462098199576842468/9Ty7sTNkj9SJLuyvl71sSKY3_IajGgFtL5QftLqKTGO2TfdyMQyCKGgcEXhk3M74vawp"
WEBHOOK_LOGS = "https://discord.com/api/webhooks/1462099070356164649/XFaaqy3Q3V-nevi1scEHIW7a1z1E-09uq5t6WLjXxPY61h6VtEvI3b-WWe_yX4Z8PAJE"

messages_fantomes = []

@app.route('/')
def home():
    return "🛡️ Escanor Online"

@app.route('/gate', methods=['POST'])
def gate():
    try:
        data = request.get_json()
        type_msg = data.get("type")
        user = data.get("user", "Anonyme")
        content = data.get("content", "")

        if type_msg == "achat":
            requests.post(WEBHOOK_BOUTIQUE, json={"content": f"👟 **Vente** | {user}: {content}"})
        elif type_msg == "special":
            requests.post(WEBHOOK_SPECIAL, json={"content": f"👁️ **Escanor** | {user}: {content}"})
        elif type_msg == "sms":
            requests.post(WEBHOOK_LOGS, json={"content": f"🔒 **SMS** | {user}: {content}"})
        elif type_msg == "chat":
            messages_fantomes.append({"u": user, "m": content})
            if len(messages_fantomes) > 15:
                messages_fantomes.pop(0)
            requests.post(WEBHOOK_LOGS, json={"content": f"💬 **Ghost** [{user}]: {content}"})

        return jsonify({"status": "ok", "chat": messages_fantomes}), 200
    except:
        return "Error", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
