from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # ← вот это обязательно

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

@app.route("/")
def index():
    return "Telegram checker running!"

@app.route("/check-subscription", methods=["POST"])
def check_subscription():
    data = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    response = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember",
        params={"chat_id": CHANNEL_USERNAME, "user_id": user_id}
    ).json()

    status = response.get("result", {}).get("status", "left")
    is_subscribed = status in ["member", "administrator", "creator"]
    return jsonify({"subscribed": is_subscribed})
