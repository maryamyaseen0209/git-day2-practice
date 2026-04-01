from __future__ import annotations
from groq import Groq
from git_day_practice.settings import settings

def generate_answer_from_prompt(prompt: str) -> str:
    try:
        if not settings.groq_api_key or settings.groq_api_key == "REPLACE_ME":
            return "GROQ_API_KEY not set in .env file"
        
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model=settings.groq_model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"Error: {str(e)}"
