from metrics import fact_recall_score, tone_accuracy_score, conciseness_clarity_score
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
SCENARIOS_PATH = "scenarios.json"
OUTPUT_JSON = "evaluation_results_modelB.json"
OUTPUT_CSV = "evaluation_results_modelB.csv"


def build_prompt_modelB(intent: str, facts: str, tone: str) -> str:
    return f"""demo prompt"""


def call_openai(prompt: str) -> str:
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()



def run_evaluation():
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY not found in .env file.")
 
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
 
    results = []