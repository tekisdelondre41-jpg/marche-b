from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

URL_DISCORD = "https://discord.com/api/webhooks/1461802698587373744/4I5FFehiroW9Ra4hBFTW_gVXKZWoSQYAc2zxAvisyhrNWbAVB1ScJZr1rKVdtDMrSKMK"

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

@app.route('/publier', methods=['POST'])
def publier():
    data = request.get_json()
    p = data.get('nom')
    prix = data.get('prix')
    requete("INSERT INTO produits (nom, prix) VALUES (?, ?)", (p, prix))
    alerte(f"📦 **Produit en attente** : {p} ({prix} F)")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    alerte("🚀 Serveur Tekis41 en ligne !")
    app.run(host='0.0.0.0', port=10000)
