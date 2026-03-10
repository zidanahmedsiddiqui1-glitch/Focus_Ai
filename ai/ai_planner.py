from datetime import datetime, timedelta
def generate_plan(subject,exam_date,hours_per_day):
    today=datetime.today()
    exam = datetime.strptime(exam_date, "%Y-%m-%d")
    days_left=(exam-today).days
    if days_left <= 0:
        print("Exam day is passed")

    total_hours = days_left*int(hours_per_day)
    plan = [f"--- Total Study Plan for {subject}: {total_hours} hours total ---"]
    for i in range(days_left):
        day = today + timedelta(days=i)
        plan.append(f"{day.strftime('%d %b')}-- study subject {subject} for {hours_per_day} hours")
        return plan