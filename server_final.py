import requests
from flask import Flask

app = Flask(__name__)

# Ton URL exacte vérifiée sur ton image 50315
URL_DISCORD = "https://discord.com/api/webhooks/1462030820028973170/7KywKTHh7yCuWdMS4ztWJma5hnpLwLGqSW7nuo_eknmj_XAG972K6FWGCh4RjWJh0j3F"
def envoyer_discord(message):
    try:
        # Cette ligne envoie réellement le message à Discord
        requests.post(URL_DISCORD, json={"content": message})
    except:
        pass

@app.route('/')
def home():
    # Cette action se déclenche quand tu ouvres le lien
    envoyer_discord("✅ Connexion réussie ! Le serveur de Tekis est en ligne.")
    return "Serveur opérationnel - Message envoyé à Discord !"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
