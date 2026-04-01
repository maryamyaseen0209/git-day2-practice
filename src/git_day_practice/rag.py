from __future__ import annotations
from git_day_practice.retrieval import search_chunks
from git_day_practice.llm_client import generate_answer_from_prompt

def build_context(results: list[dict]) -> str:
    if not results:
        return "No relevant context found."
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(
            f"[Source {i}]\n"
            f"Title: {r.get('title', 'Unknown')}\n"
            f"Text: {r.get('text', '')}\n"
        )
    return "\n".join(parts)

def build_prompt(question: str, results: list[dict]) -> str:
    context = build_context(results)
    if not results:
        return f"I don't have enough information to answer: {question}"
    return f"""
Answer using ONLY the context below.

Question: {question}

Context:
{context}

Rules:
- Use ONLY the context
- Don't invent facts
- Cite sources as [Source X]
"""

def answer_with_rag(question: str, limit: int) -> dict:
    print(f"\nProcessing: {question}")
    results = search_chunks(question, limit)
    prompt = build_prompt(question, results)
    answer = generate_answer_from_prompt(prompt)
    return {"question": question, "answer": answer, "sources": results}
