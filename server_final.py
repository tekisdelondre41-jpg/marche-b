from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

URL_DISCORD = "https://discord.com/api/webhooks/1461814425370497239/rfojjgyhsACy7B1OkjOKGf5CqqyxQzX3CLQwoaaT_WSCIgpoNZcWo35TCd_fbH33qvF_"

def alerte(txt):
    requests.post(URL_DISCORD, json={"content": txt})

def requete(sql, params=()):
    conn = sqlite3.connect('marche_b.db')
    cur = conn.cursor()
    cur.execute(sql, params)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res

@app.route('/')
def home():
    return "Serveur Tekis en ligne !"

@app.route('/test_discord')
def test():
    alerte("✅ Connexion réussie avec Spidey Bot !")
    return "Message envoyé !"

@app.route('/inscription', methods=['POST'])
def inscription():
    data = request.get_json()
    nom = data.get('nom')
    tel = data.get('telephone')
    try:
        requete("INSERT INTO utilisateurs (nom, telephone) VALUES (?, ?)", (nom, tel))
        alerte(f"👤 **Nouveau client** : {nom} ({tel})")
        return jsonify({"status": "ok"})
    except:
        return jsonify({"status": "erreur"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
