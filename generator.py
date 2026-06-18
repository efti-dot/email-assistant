from prompts import build_prompt
from google import genai

DEFAULT_MODEL = "gemini-2.5-flash"

#model call
def call_gemini(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text.strip()

#generating email
def generate_email(intent: str, facts: str, tone: str, api_key: str, model: str = DEFAULT_MODEL):
    prompt = build_prompt(intent, facts, tone)
    email_text = call_gemini(prompt, api_key, model)
    return email_text, prompt