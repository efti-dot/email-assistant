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