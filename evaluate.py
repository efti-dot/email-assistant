from dotenv import load_dotenv
import os
import json
from generator import generate_email
from metrics import fact_recall_score, tone_accuracy_score, conciseness_clarity_score
from datetime import datetime

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

        frs = fact_recall_score(generated_email, sc["facts"])
        tas = tone_accuracy_score(generated_email, sc["tone"], API_KEY)
        ccs = conciseness_clarity_score(generated_email, sc["human_reference_email"], API_KEY)
        overall = round((frs + tas + ccs) / 3, 2)

        print(f"fact_recall={frs} tone_accuracy={tas} conciseness_clarity={ccs} overall={overall}")

        #appending all the result togather
        results.append({
            "scenario_id": sc["id"],
            "intent": sc["intent"],
            "tone": sc["tone"],
            "generated_email": generated_email,
            "fact_recall": frs,
            "tone_accuracy": tas,
            "conciseness_clarity": ccs,
            "overall": overall,
        })
        n = len(results)
        
        averages = {
        "avg_fact_recall": round(sum(r["fact_recall"] for r in results) / n, 2),
        "avg_tone_accuracy": round(sum(r["tone_accuracy"] for r in results) / n, 2),
        "avg_conciseness_clarity": round(sum(r["conciseness_clarity"] for r in results) / n, 2),
        "avg_overall": round(sum(r["overall"] for r in results) / n, 2),
        }

        report = {
        "generated_at": datetime.now().isoformat()
        }


if __name__ == "__main__":
    run_evaluation()