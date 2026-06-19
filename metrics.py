from generator import call_openai
import re

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is",
    "was", "are", "were", "be", "been", "will", "with", "by", "at", "as",
    "this", "that", "has", "have", "had", "it", "its", "their", "your"
}

# For dropping stop words
def _keywords(line: str) -> list:
    words = re.findall(r"[a-zA-Z0-9#%']+", line.lower())
    return [w for w in words if w not in _STOPWORDS and len(w) > 1]

#Custom Metric 1: Fact Recall (rule-based)
def fact_recall_score(generated_email: str, facts_text: str) -> float:
    fact_lines = [f.strip() for f in facts_text.strip().split("\n") if f.strip()]
    if not fact_lines:
        return 1.0
 
    email_lower = generated_email.lower()
    recalled = 0
 
    for fact in fact_lines:
        keywords = _keywords(fact)
        if not keywords:
            continue
        matches = sum(1 for kw in keywords if kw in email_lower)
        if matches / len(keywords) >= 0.6:
            recalled += 1
 
    return round(recalled / len(fact_lines), 2)


#Custom Metric 2: Tone Accuracy (LLM-as-Judge)
def tone_accuracy_score(generated_email: str, requested_tone: str, api_key: str) -> float:
    judge_prompt = f"""You are an expert writing coach evaluating tone in professional emails.
 
    The email below was supposed to be written in a "{requested_tone}" tone.
    Rate how well the actual writing style — word choice, sentence structure,
    level of formality, and emotional register — matches that tone.
    
    Scoring guide:
    5 = The tone is unmistakable and consistent throughout. A reader would
        immediately identify it as "{requested_tone}" without being told.
    4 = The tone is clearly present and mostly consistent, with only minor
        lapses or neutral filler sentences.
    3 = The tone is somewhat present but inconsistent — it drifts toward
        generic professional writing in places.
    2 = The tone is barely noticeable. Most of the email reads as neutral
        or generic, with only one or two tonal signals.
    1 = The tone is absent or the opposite tone is used instead.
    
    Respond with ONLY a single integer between 1 and 5. No explanation.
    
    Email to evaluate:
    {generated_email}
    """
    response = call_openai(judge_prompt, api_key)
    match = re.search(r"[1-5]", response)
    score = int(match.group()) if match else 3
    return round(score / 5, 2)


#Custom Metric 3: Conciseness & Clarity (Hybrid)
def conciseness_clarity_score(generated_email: str, reference_email: str, api_key: str) -> float:
    gen_len = len(generated_email.split())
    ref_len = max(len(reference_email.split()), 1)
    ratio = gen_len / ref_len
    length_score = max(0.0, 1 - abs(1 - ratio))
 
    judge_prompt = f"""Rate the CLARITY of the email below on a scale of 1 to 5.
    5 = perfectly clear and well-structured, with no filler or rambling.
    1 = confusing, poorly organized, or padded with unnecessary text.
    
    Respond with ONLY the integer score and nothing else.

    Email:
    {generated_email}
    """
    response = call_openai(judge_prompt, api_key)
    match = re.search(r"[1-5]", response)
    clarity_score = (int(match.group()) if match else 3) / 5
 
    return round((length_score + clarity_score) / 2, 2)