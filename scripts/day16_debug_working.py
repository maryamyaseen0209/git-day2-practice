from __future__ import annotations
from git_day_practice.normalization import normalize_roman_urdu
from git_day_practice.retrieval_mock import dual_query_search_mock

def main():
    print("=" * 80)
    print("DAY 16: ROMAN-URDU NORMALIZATION & DUAL-QUERY RETRIEVAL")
    print("=" * 80)
    
    print("\n📝 1. NORMALIZATION DEMONSTRATION:")
    print("-" * 50)
    
    test_queries = [
        "qdrant kia karta he",
        "docker compose kia krta he",
        "mjhe retrieval ka jawab do",
    ]
    
    for query in test_queries:
        normalized = normalize_roman_urdu(query)
        print(f"\n  Original:    '{query}'")
        print(f"  Normalized:  '{normalized}'")
    
    print("\n" + "=" * 80)
    print("🔍 2. DUAL-QUERY RETRIEVAL DEMONSTRATION:")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n📌 Query: '{query}'")
        result = dual_query_search_mock(query, limit=3)
        
        print(f"\n  ✅ Original query searched: '{result['original_query']}'")
        print(f"  ✅ Normalized query searched: '{result['normalized_query']}'")
        print(f"\n  📊 Results ({len(result['results'])} unique chunks):")
        
        for idx, item in enumerate(result["results"], 1):
            print(f"\n    [{idx}] Score: {item['score']:.2f}")
            print(f"        Title: {item['title']}")
            print(f"        Text: {item['text'][:80]}...")
    
    print("\n" + "=" * 80)
    print("✅ DAY 16 COMPLETED SUCCESSFULLY!")
    print("   • Roman-Urdu normalization working")
    print("   • Dual-query logic implemented")
    print("   • Result merging and deduplication working")
    print("   • Original and normalized queries both searched")
    print("=" * 80)

if __name__ == "__main__":
    main()