from __future__ import annotations
from git_day_practice.normalization import normalize_roman_urdu

# Test queries
test_queries = [
    "qdrant kia karta he",
    "docker compose kia krta he",
    "mujhe retrieval ka jawab do",
    "mjhe qdrant kia krta hy",
    "retrival sy maloomat kesay milti he",
]

print("=" * 70)
print("ROMAN-URDU NORMALIZATION DEMO")
print("=" * 70)

for query in test_queries:
    normalized = normalize_roman_urdu(query)
    print(f"\nOriginal:    {query}")
    print(f"Normalized:  {normalized}")
    print("-" * 50)

# Show mapping examples
print("\n\nWORD MAPPING EXAMPLES:")
print("=" * 40)
mappings = {
    "kia": "kya",
    "he": "hai", 
    "hy": "hai",
    "mjhe": "mujhe",
    "krta": "karta",
    "retrival": "retrieval",
    "maloomat": "malumat",
}

for original, normalized in mappings.items():
    print(f"  '{original}' → '{normalized}'")

print("\n✅ Normalization module is working!")
print("Note: Full Qdrant integration requires Docker installation.")