from datetime import datetime, timedelta

def generate_study_plan(subjects, exam_date, hours_per_day):

    today = datetime.today()
    exam = datetime.strptime(exam_date, "%Y-%m-%d")

    days_left = (exam - today).days

    plan = []

    for day in range(days_left):

        study_day = today + timedelta(days=day)

        daily_plan = {
            "date": study_day.strftime("%Y-%m-%d"),
            "subjects": []
        }

        hours_each = round(hours_per_day / len(subjects),1)

        for subject in subjects:
            daily_plan["subjects"].append({
                "subject": subject,
                "hours": hours_each
            })

        plan.append(daily_plan)

    return plan