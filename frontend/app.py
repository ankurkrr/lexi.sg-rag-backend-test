from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:8080/query"  # FastAPI backend URL

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.form.get("query")
    if not user_query:
        return jsonify({"error": "No query provided."}), 400
    try:
        response = requests.post(API_URL, json={"query": user_query}, timeout=120)
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "answer": data.get("answer", "No answer."),
                "citations": data.get("citations", [])
            })
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
