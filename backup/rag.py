from __future__ import annotations

from git_day_practice.llm_client import generate_answer_from_prompt
from git_day_practice.retrieval import search_chunks

def build_context_block(results: list[dict]) -> str:
    """Build a formatted context block from search results."""
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
    """Build a grounded prompt for the LLM."""
    context = build_context_block(results)
    
    return f"""
Answer the question using only the context below.

Question: {question}

Context:
{context}

Rules:
- Use only the provided context.
- Do not invent facts.
- If the answer is not supported by the context, say that clearly.
- Mention supporting sources using the source numbers.
""".strip()

def answer_with_rag(question: str, limit: int) -> dict:
    """Orchestrate the complete RAG pipeline."""
    # Retrieve relevant chunks
    results = search_chunks(question, limit)
    
    # Build prompt with context
    prompt = build_rag_prompt(question, results)
    
    # Generate answer using LLM
    answer = generate_answer_from_prompt(prompt)
    
    return {
        "question": question,
        "answer": answer,
        "sources": results,
    }