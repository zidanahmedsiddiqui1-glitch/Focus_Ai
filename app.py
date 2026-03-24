from flask import Flask, render_template, request
from ai.chatbot import chatbot_response
from database import get_dashboard_data, get_recent_activity, add_task, complete_task, get_tasks, set_exam_date
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
@app.route("/chat-page")
def chat_page():
    return render_template("chat.html")
@app.route("/planner-page")
def planner_page():
    return render_template("planner.html")
@app.route("/dashboard-data")
def dashboard_data():
    return jsonify(get_dashboard_data())

@app.route("/get-tasks")
def tasks():
    return jsonify(get_tasks())

@app.route("/add-task", methods=["POST"])
def new_task():
    task_name = request.json["task_name"]
    add_task(task_name)
    return jsonify({"status": "success"})

@app.route("/complete-task/<int:task_id>", methods=["POST"])
def close_task(task_id):
    complete_task(task_id)
    return jsonify({"status": "success"})

@app.route("/set-exam-date", methods=["POST"])
def update_exam_date():
    exam_date = request.json["exam_date"]
    set_exam_date(exam_date)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)