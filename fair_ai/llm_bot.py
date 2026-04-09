import requests

# 🔥 GLOBAL MEMORY
chat_history = []

# -------------------------------
# FALLBACK SYSTEM
# -------------------------------
def fallback_response(user_input, context=None):
    msg = user_input.lower()

    context_info = ""
    if context:
        di = context.get("disparate_impact")
        risk = context.get("risk_level")
        context_info = f"(Dataset DI={di}, Risk={risk}) "

    if "bias" in msg:
        return context_info + "Bias means unfair preference toward a group."

    elif "fairness" in msg:
        return context_info + "Fairness ensures equal treatment of all groups."

    elif "model" in msg:
        return context_info + "Model analyzes fairness and predictions."

    elif "risk" in msg:
        return context_info + "Risk indicates potential unfair decisions."

    elif "improve" in msg:
        return context_info + "Use mitigation techniques like reweighting."

    else:
        return context_info + "System is running in fallback mode."

# -------------------------------
# MAIN AI FUNCTION
# -------------------------------
def get_response(user_input, context=None):
    global chat_history

    # 🧠 ADD USER MESSAGE
    chat_history.append({"role": "user", "content": user_input})

    try:
        api_key = "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"   # 🔥 IMPORTANT

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 🔥 CONTEXT ADD
        context_msg = ""
        if context:
            context_msg = f"Dataset info: DI={context.get('disparate_impact')}, Risk={context.get('risk_level')}"

        messages = [
            {"role": "system", "content": "You are an AI assistant for fairness, bias detection, and ML explainability."},
            {"role": "system", "content": context_msg}
        ] + chat_history[-6:]   # 🔥 last 6 messages (memory)

        data = {
            "model": "openrouter/auto",
            "messages": messages
        }

        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()

        # ✅ SUCCESS
        if "choices" in res_json:
            reply = res_json['choices'][0]['message']['content']

            # 🧠 SAVE AI RESPONSE
            chat_history.append({"role": "assistant", "content": reply})

            return reply

        # ❌ fallback
        return fallback_response(user_input, context)

    except Exception as e:
        return fallback_response(user_input, context)