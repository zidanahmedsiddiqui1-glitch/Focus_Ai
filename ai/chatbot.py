def chatbot_response(message):

    message = message.lower()

    if "study plan" in message:
        return "Great! What subject are you preparing for?"

    elif "physics" in message or "math" in message or "chemistry" in message:
        return "Nice. When is your exam?"

    elif "exam" in message:
        return "How many hours can you study daily?"

    else:
        return "I can help you create a study plan. Tell me your subject."