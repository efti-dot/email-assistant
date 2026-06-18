from dotenv import load_dotenv
import os
import json
from generator import generate_email
from metrics import fact_recall_score, tone_accuracy_score, conciseness_clarity_score

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
SCENARIOS_PATH = "scenarios.json"


def run_evaluation():
    #print("Evaluating...")
    if not API_KEY:
        raise RuntimeError("Gemini api key not found. Please set it in a .env file.")
    
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    results = []

    for sc in scenarios:
        print(f"Scenario {sc['id']:>2}: {sc['intent']} ({sc['tone']}) ... ", end="", flush=True)

        generated_email, _ = generate_email(
            intent=sc["intent"],
            facts=sc["facts"],
            tone=sc["tone"],
            api_key=API_KEY,
        )

        fr = fact_recall_score(generated_email, sc["facts"])
        ta = tone_accuracy_score(generated_email, sc["tone"], API_KEY)
        cc = conciseness_clarity_score(generated_email, sc["human_reference_email"], API_KEY)
        overall = round((fr + ta + cc) / 3, 2)


if __name__ == "__main__":
    run_evaluation()