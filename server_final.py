from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

URL_DISCORD = "https://discord.com/api/webhooks/1462030820028973170/7KywKTHh7yCuWdMS4ztWJma5hnpLwLGqSW7nuo_eknmj_XAG972K6FWGCh4RjWJh0j3F"

@app.route('/')
def home():
    return "Serveur Tekis en ligne !"

@app.route('/inscription', methods=['POST'])
def inscription():
    try:
        data = request.get_json()
        numero = data.get("numero", "Inconnu")
        achat = data.get("achat", "Inconnu")
        
        # Le 'f' devant les guillemets est obligatoire :
        contenu = f"🚀 **Nouvelle commande !**\n📞 Numéro : {numero}\n👟 Article : {achat}"
        
        requests.post(URL_DISCORD, json={"content": contenu})
        return jsonify({"status": "succès"}), 200
    except Exception as e:
        return jsonify({"status": "erreur", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
