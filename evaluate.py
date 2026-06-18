from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def run_evaluation():
    #print("Evaluating...")
    if not API_KEY:
        raise RuntimeError("Gemini api key not found. Please set it in a .env file.")



if __name__ == "__main__":
    run_evaluation()