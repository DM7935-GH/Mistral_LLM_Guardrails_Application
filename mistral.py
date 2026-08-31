import os
import json
import requests
import time

API_KEY = os.environ.get("MISTRAL_API_KEY")
mistral_model = "mistral-small-latest"


def new_prompt_mistral (prompt : str):
    mistral_url = "https://api.mistral.ai/v1/chat/completions"
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": mistral_model,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = None
    attempts = 0

    while attempts < 5:
        response = requests.post(mistral_url, json=data, headers=headers)

        if response.status_code == 429:
            # The Mistral model's server is currently overloaded
            attempts += 1
            print(f"Service capacity exceeded for '{mistral_model}'. Retrying in 15 seconds (attempt {attempts}/5)")
            time.sleep(15)
        elif response.status_code != 200:
            return response.status_code
        else:
            return response.json()["choices"][0]["message"]["content"]
    return 500

#mistral_request = new_prompt_mistral("What is the melting point of silver?")
#print(mistral_request)