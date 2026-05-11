from __future__ import annotations
import json
from typing import Any
from git_day_practice.guardrails import choose_rag_action
from git_day_practice.llm_client import generate_answer_from_prompt
from git_day_practice.retrieval import dual_query_search


def build_agent_plan(question: str) -> list[str]:
    """Create an explicit plan for the agent to follow."""
    return [
        "Step 1: Normalize and inspect the question.",
        "Step 2: Retrieve relevant chunks from Qdrant using dual-query search.",
        "Step 3: Judge retrieval quality and decide whether to answer, clarify, or refuse.",
        "Step 4: Generate an answer only if the evidence is sufficient.",
    ]


def build_context_block(results: list[dict]) -> str:
    """Build a formatted context block from retrieval results."""
    parts: list[str] = []
    
    for idx, item in enumerate(results, start=1):
        parts.append(
            f"[Source {idx}]\n"
            f"doc_id: {item['doc_id']}\n"
            f"chunk_id: {item['chunk_id']}\n"
            f"title: {item.get('title', 'Unknown')}\n"
            f"text: {item['text']}\n"
        )
    
    return "\n".join(parts)


def build_agent_prompt(question: str, results: list[dict]) -> str:
    """Build the prompt for answer generation."""
    context = build_context_block(results)
    
    return f"""Answer the question using only the context below.

Question: {question}

Context:
{context}

Rules:
- Use only the provided context.
- Do not invent facts.
- If the answer is not supported by the context, say that clearly.
- Mention supporting sources using the source numbers (e.g., [Source 1]).
- Be concise and accurate.

Answer:""".strip()


def build_confidence_dict(results: list[dict]) -> dict:
    """Build confidence object from results."""
    if not results:
        return {
            "top_score": 0.0,
            "avg_score": 0.0,
            "result_count": 0
        }
    
    scores = [r.get("score", 0.0) for r in results]
    return {
        "top_score": max(scores),
        "avg_score": sum(scores) / len(scores),
        "result_count": len(results)
    }


def run_agent_loop(question: str, limit: int = 3) -> dict[str, Any]:
    """
    Run the controlled agent loop:
    Plan -> Retrieve -> Judge -> Answer/Clarify/Refuse
    """
    # Step 1: Plan
    plan = build_agent_plan(question)
    
    # Step 2: Retrieve
    retrieval_payload = dual_query_search(question, limit)
    results = retrieval_payload["results"]
    normalized_query = retrieval_payload["normalized_query"]
    
    # Step 3: Judge - use existing guardrails
    decision = choose_rag_action(question, results)
    
    # Build confidence object
    confidence = build_confidence_dict(results)
    
    # Step 4: Decide action based on judgment
    if decision["action"] == "clarify":
        return {
            "question": question,
            "normalized_query": normalized_query,
            "plan": plan,
            "action": "clarify",
            "reason": decision["reason"],
            "answer": "I'm not sure I understand. Please clarify your question with more specific details.",
            "sources": results,
            "confidence": confidence,
        }
    
    if decision["action"] == "refuse":
        return {
            "question": question,
            "normalized_query": normalized_query,
            "plan": plan,
            "action": "refuse",
            "reason": decision["reason"],
            "answer": "I cannot answer that question as I don't have enough reliable context.",
            "sources": results,
            "confidence": confidence,
        }
    
    # Action is "answer" - generate the response
    prompt = build_agent_prompt(question, results)
    answer = generate_answer_from_prompt(prompt)
    
    return {
        "question": question,
        "normalized_query": normalized_query,
        "plan": plan,
        "action": "answer",
        "reason": decision["reason"],
        "answer": answer,
        "sources": results,
        "confidence": confidence,
    }