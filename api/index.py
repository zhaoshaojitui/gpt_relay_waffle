from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# 从环境变量读取 Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "✅ GPT Relay Running on Vercel!"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        message = data.get("message", "")
        if not message:
            return jsonify({"error": "Missing message"}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )

        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Vercel 会自动识别这个 Flask app
app = app