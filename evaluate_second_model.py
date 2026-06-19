from metrics import fact_recall_score, tone_accuracy_score, conciseness_clarity_score
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
SCENARIOS_PATH = "scenarios.json"
OUTPUT_JSON = "evaluation_results_modelB.json"
OUTPUT_CSV = "evaluation_results_modelB.csv"

