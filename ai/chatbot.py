import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ai.planner_engine import generate_study_plan
import json

load_dotenv()

# Initialize the new google-genai client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration for the model
MODEL_NAME ="gemini-flash-latest"
SYSTEM_INSTRUCTION = """
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

# Sessions to maintain chat history
sessions = {}

def chatbot_response(message, session_id="default"):
    # In the new google-genai SDK, history is a list of Content objects
    # For simplicity, we can just pass the string history if using start_chat
    if session_id not in sessions:
        sessions[session_id] = client.chats.create(
            model=MODEL_NAME,
            config={
                'system_instruction': SYSTEM_INSTRUCTION
            }
        )

    chat = sessions[session_id]

    try:
        response = chat.send_message(message)
        reply = response.text.strip()
    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        return "Sorry, I encountered an error. Please try again later."

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

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error parsing plan JSON: {e}")
            return reply

    return reply