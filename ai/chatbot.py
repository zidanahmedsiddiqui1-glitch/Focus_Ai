import google.generativeai as genai
from ai.planner_engine import generate_study_plan
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
You are Focus AI, a smart productivity assistant for students.
You help students with:
1. Creating personalized study plans
2. Managing personal commitments (gym, prayer, sleep, etc.)
3. Summarizing notes
4. Staying focused and avoiding distractions

When a student wants a study plan, collect this information conversationally:
- Subjects they want to study
- Their daily commitments (gym, prayer, etc.) with timings if provided
- Their exam date (ask them to provide it in YYYY-MM-DD format)
- How many hours they can study per day

Once you have ALL of that information, respond with ONLY this JSON and nothing else:
{
  "action": "generate_plan",
  "subjects": ["Math", "Physics"],
  "exam_date": "2026-04-15",
  "hours": 3,
  "commitments": ["gym 7am-8am", "prayer 5pm"]
}

For all other conversations, respond naturally and helpfully.
If the student asks about focus tips, motivation, time management — answer directly.
Keep responses concise, friendly and encouraging. Use emojis where suitable.
"""
)

sessions = {}

def chatbot_response(message, session_id="default"):
    if session_id not in sessions:
        sessions[session_id] = model.start_chat(history=[])

    chat = sessions[session_id]

    response = chat.send_message(message)
    reply = response.text.strip()

    # Check if Gemini wants to generate a plan
    if '"action": "generate_plan"' in reply:
        try:
            json_start = reply.index("{")
            json_end = reply.rindex("}") + 1
            plan_data = json.loads(reply[json_start:json_end])

            plan = generate_study_plan(
                plan_data["subjects"],
                plan_data["exam_date"],
                plan_data["hours"],
                plan_data.get("commitments", [])
            )

            if not plan:
                return "⚠️ Your exam date seems to be in the past. Could you give me a future date?"

            plan_text = f"📚 Your Study Plan is ready! ({len(plan)} days until exam)\n"
            for day in plan[:3]:
                plan_text += f"\n📅 {day['date']}\n"
                for subject in day["subjects"]:
                    plan_text += f"  • {subject['subject'].title()} → {subject['hours']} hrs\n"
                if day["commitments"]:
                    plan_text += f"  🔒 Commitments: {', '.join(day['commitments'])}\n"
            if len(plan) > 3:
                plan_text += f"\n...and {len(plan) - 3} more days! 💪"
            plan_text += "\n\nSay 'new plan' anytime to create another one!"
            return plan_text

        except (json.JSONDecodeError, KeyError, ValueError):
            return reply

    return reply