# Email Generation Assistant

A Streamlit web app that generates professional emails from three inputs — **Intent**, **Key Facts**, and **Tone** — using the OpenAI GPT-4o-mini API.

---

## Project Structure

```
email-assistant/
├── app.py                          # Streamlit UI (Part 1)
├── generator.py                    # Shared OpenAI call logic
├── prompts.py                      # Prompt template (Model A — advanced)
├── metrics.py                      # 3 custom evaluation metrics (Part 2)
├── scenarios.json                  # 10 test scenarios + human reference emails
├── evaluate.py                     # Runs Model A evaluation, writes results
├── evaluate_second_model.py        # Runs Model B evaluation (Part 3 comparison)
├── evaluation_results.json         # Model A full report
├── evaluation_results.csv          # Model A scores
├── evaluation_results_modelB.json  # Model B full report
├── evaluation_results_modelB.csv   # Model B scores
├── requirements.txt                # Python dependencies
├── .env.example                    # Template for API key
└── README.md
```

---

## Prompting Technique

This assistant uses a combined **Role-Playing + Chain-of-Thought + Per-Tone Guide** strategy (see `prompts.py`):

- **Role-Playing** — anchors the model to an "expert executive assistant" persona, calibrating professionalism and vocabulary automatically.
- **Chain-of-Thought** — forces the model to reason through intent → facts → tone → structure *before* drafting, improving fact recall and tone accuracy.
- **Per-Tone Guide** — provides concrete, tone-specific instructions (e.g. Urgent → *"Short sentences. Lead with the critical information immediately."*) so the model commits to the requested tone rather than defaulting to generic professional writing.

These three techniques directly target the dimensions measured by the 3 custom evaluation metrics in Part 2.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/email-assistant.git
cd email-assistant
```

### 2. Create a virtual environment

```bash
python -m venv myenv
```

Windows:
```bash
myenv\Scripts\activate
```

Mac/Linux:
```bash
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy `.env.example` to `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
```

Get a key at: https://platform.openai.com/api-keys

---

## Running the Assistant (Part 1)

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`. Enter your intent, key facts, and choose a tone, then click **Generate Email**.

---

## Running the Evaluation (Part 2)

```bash
python evaluate.py
```

Runs all 10 scenarios through the assistant (Model A) and scores them using the 3 custom metrics. Outputs:

- `evaluation_results.json` — full report including metric definitions and generated emails
- `evaluation_results.csv` — flat scores for spreadsheet review

---

## Running the Model Comparison (Part 3)

```bash
python evaluate_second_model.py
```

Runs the same 10 scenarios using Model B (simple prompt, no per-tone guide). Outputs:

- `evaluation_results_modelB.json`
- `evaluation_results_modelB.csv`

---

## The 3 Custom Metrics

| Metric | Type | What it measures |
|---|---|---|
| `fact_recall` | Rule-based | % of supplied key facts whose keywords appear in the output |
| `tone_accuracy` | LLM-as-Judge | GPT-4o-mini rates 1–5 how well writing style matches requested tone |
| `conciseness_clarity` | Hybrid | Average of length-ratio score vs reference email + LLM clarity rating |

---

## Requirements

```
streamlit
openai
python-dotenv
```

Install with:

```bash
pip install -r requirements.txt
```
