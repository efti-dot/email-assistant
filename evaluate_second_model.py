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


METRIC_DEFINITIONS = {
    "fact_recall": (
        "Rule-based. For each supplied key fact, checks whether at least "
        "60% of its meaningful keywords appear in the generated email. "
        "Score = (facts recalled) / (total facts)."
    ),
    "tone_accuracy": (
        "LLM-as-Judge. GPT-4o-mini rates 1-5 how well the email's actual "
        "writing style matches the requested tone. Score = rating / 5."
    ),
    "conciseness_clarity": (
        "Hybrid. Averages (a) a length-ratio score vs the human reference "
        "email, and (b) an LLM clarity rating 1-5."
    ),
}


def run_evaluation():
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY not found in .env file.")
 
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
 
    results = []
    for sc in scenarios:
        print(f"Scenario {sc['id']:>2}: {sc['intent']} ({sc['tone']}) ... ", end="", flush=True)

        #model call
        prompt = build_prompt_modelB(sc["intent"], sc["facts"], sc["tone"])
        generated_email = call_openai(prompt)

        #score
        frs      = fact_recall_score(generated_email, sc["facts"])
        tas      = tone_accuracy_score(generated_email, sc["tone"], API_KEY)
        ccs      = conciseness_clarity_score(generated_email, sc["human_reference_email"], API_KEY)
        overall = round((frs + tas + ccs) / 3, 2)
 
        print(f"fact_recall={frs} tone_accuracy={tas} conciseness_clarity={ccs} overall={overall}")
 
        results.append({
            "scenario_id":         sc["id"],
            "intent":              sc["intent"],
            "tone":                sc["tone"],
            "generated_email":     generated_email,
            "fact_recall":         frs,
            "tone_accuracy":       tas,
            "conciseness_clarity": ccs,
            "overall":             overall,
        })