from flask import Flask, render_template, request
from ai.chatbot import chatbot_response
from flask import jsonify
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    reply = chatbot_response(user_message)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)