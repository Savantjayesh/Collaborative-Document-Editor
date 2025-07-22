import os
import requests
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------------------
# 1. LanguageTool Grammar Check
# ------------------------------

def split_text(text, max_length=1500):
    parts = []
    while len(text) > max_length:
        split_at = text.rfind('.', 0, max_length)
        if split_at == -1:
            split_at = max_length
        parts.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        parts.append(text)
    return parts

def check_grammar(text):
    try:
        suggestions = []

        for chunk in split_text(text):
            response = requests.post(
                'https://api.languagetoolplus.com/v2/check',
                data={'text': chunk, 'language': 'en-US'},
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            if response.status_code != 200:
                print(f"Chunk error: {response.status_code}")
                continue

            result = response.json()
            suggestions.extend(result.get('matches', []))

        return {"matches": suggestions}
    except Exception as e:
        print("Error in grammar_suggestions:", str(e))
        return {"error": str(e)}



# ------------------------------
# 2. OpenAI Suggestion (GPT 3.5/4)
# ------------------------------
def suggest_edit(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "Improve this text for grammar, clarity, and professionalism."},
                {"role": "user", "content": text}
            ],
            temperature=0.7
        )

        improved_text = response["choices"][0]["message"]["content"].strip()

        return {
            "suggested": improved_text,
            "tokens_used": response.get("usage", {}).get("total_tokens"),
            "model": response.get("model")
        }

    except Exception as e:
        return {"error": str(e)}
