from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

URL_DISCORD = "https://discord.com/api/webhooks/1462030820028973170/7KywKTHh7yCuWdMS4ztWJma5hnpLwLGqSW7nuo_eknmj_XAG972K6FWGCh4RjWJh0j3F"

@app.route('/')
def home():
    # Ce bloc va forcer un envoi à Discord pour tester le circuit
    try:
        requests.post(URL_DISCORD, json={"content": "✅ TEST DIRECT : Le serveur Render parle bien à Discord !"})
        return "Serveur en ligne - Test Discord envoyé !"
    except:
        return "Serveur en ligne - Mais échec de l'envoi Discord."

@app.route('/inscription', methods=['POST'])
def inscription():
    try:
        data = request.get_json()
        numero = data.get("numero", "Inconnu")
        achat = data.get("achat", "Inconnu")
        message = f"🚀 **Nouvelle commande !**\n📞 Numéro : {numero}\n👟 Article : {achat}"
        requests.post(URL_DISCORD, json={"content": message})
        return jsonify({"status": "succès"}), 200
    except:
        return jsonify({"status": "erreur"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
