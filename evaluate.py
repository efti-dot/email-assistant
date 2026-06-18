from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def run_evaluation():
    print("Evaluating...")



if __name__ == "__main__":
    run_evaluation()