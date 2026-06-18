from generator import call_gemini
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