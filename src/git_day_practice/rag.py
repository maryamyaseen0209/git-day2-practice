from __future__ import annotations
from git_day_practice.llm_client import generate_answer_from_prompt
from git_day_practice.retrieval import dual_query_search

def build_context_block(results: list[dict]) -> str:
    parts: list[str] = []
    for idx, item in enumerate(results, start=1):
        parts.append(
            f"[Source {idx}]\n"
            f"doc_id: {item['doc_id']}\n"
            f"chunk_id: {item['chunk_id']}\n"
            f"title: {item['title']}\n"
            f"text: {item['text']}\n"
        )
    return "\n".join(parts)

def build_rag_prompt(question: str, results: list[dict]) -> str:
    context = build_context_block(results)
    return f"""Answer the question using only the context below.

Question: {question}

Context: {context}

Rules:
- Use only the provided context.
- Do not invent facts.
- If the answer is not supported by the context, say that clearly.
- Mention supporting sources using the source numbers.

Answer:""".strip()

def answer_with_rag(question: str, limit: int = 3) -> dict:
    """Main RAG function - called by the API endpoint"""
    retrieval_payload = dual_query_search(question, limit)
    results = retrieval_payload["results"]
    
    if not results:
        return {
            "question": question,
            "normalized_query": retrieval_payload["normalized_query"],
            "answer": "I couldn't find any relevant information to answer your question.",
            "sources": [],
        }
    
    prompt = build_rag_prompt(question, results)
    answer = generate_answer_from_prompt(prompt)
    
    return {
        "question": question,
        "normalized_query": retrieval_payload["normalized_query"],
        "answer": answer,
        "sources": results,
    }

# Alias for compatibility with Day 18 expectations
rag_endpoint = answer_with_rag