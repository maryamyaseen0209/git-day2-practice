from __future__ import annotations
import re

ROMAN_URDU_REPLACEMENTS = {
    "kia": "kya",
    "kya": "kya",
    "kr": "kar",
    "krta": "karta",
    "krli": "karti",
    "krna": "karna",
    "he": "hai",
    "hy": "hai",
    "hn": "hain",
    "mje": "mujhe",
    "muje": "mujhe",
    "mjhe": "mujhe",
    "qdrnt": "qdrant",
    "retrival": "retrieval",
    "maloomat": "malumat",
    "javab": "jawab",
    "btado": "bata do",
    "btao": "batao",
}

def basic_cleanup(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text

def normalize_roman_urdu(text: str) -> str:
    cleaned = basic_cleanup(text)
    words = cleaned.split()
    normalized_words = [ROMAN_URDU_REPLACEMENTS.get(word, word) for word in words]
    normalized = " ".join(normalized_words)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized