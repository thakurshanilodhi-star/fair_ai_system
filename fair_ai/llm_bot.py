# OpenRouter LLM + fallback integration

import requests
import os

from fallback import fallback_response   # external fallback use कर रहे हैं


def get_response(user_input, context):

    api_key = os.getenv("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")

    # अगर API key नहीं है → fallback
    if not api_key:
        return fallback_response(user_input, context)

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant that explains bias and fairness in machine learning in simple terms."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        else:
            return fallback_response(user_input, context)

    except:
        return fallback_response(user_input, context)