from flask import Flask, render_template, request
from ai_planner import generate_plan
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/generate", methods = ["POST"])
def generate():
    subject = request.form["subject"]
    exam_date = request.form["exam_date"]
    hours = request.form["hours"]

    plan = generate_plan(subject,exam_date,hours)
    return render_template("plan.html", plan=plan)
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
if __name__ == "__main__":
    app.run(debug=True)