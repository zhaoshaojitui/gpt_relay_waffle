from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 从环境变量读取 Key（部署后 Vercel 会自动注入）
openai.api_key = os.getenv("OPENAI_API_KEY")

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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )

        return jsonify({"reply": response["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 这是 Vercel 运行时会寻找的对象
def handler(event, context):
    return app(event, context)