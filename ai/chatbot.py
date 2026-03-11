from ai.planner_engine import generate_study_plan

# Simple memory for conversation
user_data = {
    "subjects": None,
    "exam_date": None,
    "hours": None
}

def chatbot_response(message):

    message = message.lower()

    # Ask for subjects
    if "study plan" in message:
        return "Sure! What subjects do you want to study? (Example: Math, Physics)"

    # Save subjects
    if "," in message and user_data["subjects"] is None:
        subjects = [s.strip() for s in message.split(",")]
        user_data["subjects"] = subjects
        return "Great. What is your exam date? (YYYY-MM-DD)"

    # Save exam date
    if "-" in message and user_data["exam_date"] is None:
        user_data["exam_date"] = message
        return "How many hours can you study per day?"

    # Save hours
    if message.isdigit() and user_data["hours"] is None:
        user_data["hours"] = int(message)

        plan = generate_study_plan(
            user_data["subjects"],
            user_data["exam_date"],
            user_data["hours"]
        )

        # Convert plan to readable text
        plan_text = ""

        for day in plan[:3]:  # show first 3 days
            plan_text += f"\n📅 {day['date']}\n"

            for subject in day["subjects"]:
                plan_text += f"• {subject['subject'].title()} → {subject['hours']} hours\n"

        return "📚 Your Study Plan:\n" + plan_text



    return "I can help you create a study plan. Just say 'I want a study plan'."