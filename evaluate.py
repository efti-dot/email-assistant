from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
SCENARIOS_PATH = "scenarios.json"

def run_evaluation():
    #print("Evaluating...")
    if not API_KEY:
        raise RuntimeError("Gemini api key not found. Please set it in a .env file.")
    
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    result = []



if __name__ == "__main__":
    run_evaluation()