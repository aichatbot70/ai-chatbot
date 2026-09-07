from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is empty"}), 400

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=user_message
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "error": "AI se response nahi aa raha."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)