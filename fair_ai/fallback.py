# यह file fallback logic के लिए है

def fallback_response(user_input, context):
    user_input = user_input.lower()

    if "bias" in user_input:
        return "Bias का मतलब है model का unfair behavior।"

    if "fix" in user_input or "improve" in user_input:
        return "आप data balancing या fairness techniques use कर सकते हैं।"

    if "result" in user_input:
        return f"Current bias status: {context.get('bias', 'Unknown')}"

    return "System limited mode में चल रहा है। आप bias या model के बारे में पूछ सकते हैं।"