import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Ton URL complète de l'image 50315
URL_DISCORD = "https://discord.com/api/webhooks/1461814425370497239/rfojjgyhsACy7B1OkjOKGf5CqqyxQzX3CLQwoaaT_WSClgpoNZcWo35TCd_fbH33qvF_"

def envoyer_discord(message):
    requests.post(URL_DISCORD, json={"content": message})

@app.route('/')
def home():
    envoyer_discord("🚀 Le serveur est en ligne !")
    return "Serveur opérationnel"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
