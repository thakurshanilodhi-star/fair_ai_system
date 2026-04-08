import requests

# -------------------------------
# Fallback system (rule-based)
# -------------------------------
def fallback_response(user_input):
    user_input = user_input.lower()

    if "bias" in user_input:
        return "Bias means unfair preference toward a group in data or model."

    elif "fairness" in user_input:
        return "Fairness ensures equal treatment of all groups in predictions."

    elif "model" in user_input:
        return "The system uses machine learning models to analyze fairness."

    elif "risk" in user_input:
        return "Risk indicates how unfair the model predictions might be."

    else:
        return "System is in fallback mode. Please check API connection."


# -------------------------------
# Main AI function
# -------------------------------
def get_response(user_input, context):

    try:
        api_key = "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"   # Api key
        
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openrouter/auto",
    
                "messages": [
                {"role": "system", "content": "You are an AI assistant for fairness and bias detection."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        res_json = response.json()

        # अगर API सही response दे
        if "choices" in res_json:
            return res_json['choices'][0]['message']['content']

        # अगर कुछ गड़बड़
        return fallback_response(user_input)

    except Exception as e:
        return fallback_response(user_input)