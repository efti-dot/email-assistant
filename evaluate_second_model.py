from metrics import fact_recall_score, tone_accuracy_score, conciseness_clarity_score
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import datetime
import csv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
SCENARIOS_PATH = "scenarios.json"
OUTPUT_JSON = "evaluation_results_modelB.json"
OUTPUT_CSV = "evaluation_results_modelB.csv"


def build_prompt_modelB(intent: str, facts: str, tone: str) -> str:
    return f"""You are a professional executive assistant with 15+ years of experience writing business correspondence. You are known for emails that are clear, appropriately toned, and never miss a key detail.
 
Before writing, reason through the following steps internally:
1. Identify the core purpose (intent) of this email.
2. List every key fact provided below and decide the most natural place for each one in the email body. Every single fact MUST appear somewhere in the final email -- do not drop or merge facts together in a way that loses information.
3. Decide on vocabulary, sentence length, and structure that genuinely matches the requested tone: {tone}. Do not just mention the tone -- the writing itself must demonstrate it.
4. Draft the email using a clear structure: a greeting, a short opening that states the purpose, one to two short paragraphs that weave in the facts naturally, a clear closing line or call-to-action, and a sign-off.
 
After reasoning through the steps above, output ONLY the final email. Do not show your reasoning steps, do not add any notes, headers, or explanations before or after the email.
 
Intent: {intent}
 
Key Facts:
{facts}
 
Tone: {tone}
 
Email:"""


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

    n = len(results)
    averages = {
            "avg_fact_recall":         round(sum(r["fact_recall"] for r in results) / n, 2),
            "avg_tone_accuracy":       round(sum(r["tone_accuracy"] for r in results) / n, 2),
            "avg_conciseness_clarity": round(sum(r["conciseness_clarity"] for r in results) / n, 2),
            "avg_overall":             round(sum(r["overall"] for r in results) / n, 2),
    }

    report = {
        "model":              "gpt-4o-mini",
        "prompt_strategy":    "Simple (Role-Play + CoT, no per-tone guide)",
        "metric_definitions": METRIC_DEFINITIONS,
        "results":            results,
        "averages":           averages,
    }
 
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
 
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "scenario_id", "intent", "tone",
            "fact_recall", "tone_accuracy", "conciseness_clarity", "overall"
        ])
        writer.writeheader()
        for r in results:
            writer.writerow({k: r[k] for k in writer.fieldnames})
 
    print("\n=== Model B Averages ===")
    for k, v in averages.items():
        print(f"  {k}: {v}")
    print(f"\nFull report : {OUTPUT_JSON}")
    print(f"CSV scores  : {OUTPUT_CSV}")


if __name__ == "__main__":
    run_evaluation()