from __future__ import annotations
from statistics import mean
from git_day_practice.settings import settings

def is_query_too_vague(question: str) -> bool:
    stripped = question.strip().lower()
    vague_queries = {"tell me", "explain", "what is this", "help", "answer this", "hi", "hello"}
    if stripped in vague_queries or len(stripped.split()) <= 1:
        return True
    return False

def compute_confidence(results: list[dict]) -> dict:
    if not results:
        return {"top_score": 0.0, "avg_score": 0.0, "result_count": 0}
    scores = [item["score"] for item in results]
    return {
        "top_score": max(scores),
        "avg_score": mean(scores),
        "result_count": len(results),
    }

def choose_rag_action(question: str, results: list[dict]) -> dict:
    confidence = compute_confidence(results)
    
    if settings.enable_clarify_behavior and is_query_too_vague(question):
        return {
            "action": "clarify",
            "reason": "Question is too vague or underspecified.",
            "confidence": confidence,
        }
    
    if settings.enable_refuse_behavior:
        if confidence["result_count"] < settings.min_results_for_answer:
            return {
                "action": "refuse",
                "reason": f"Not enough results (need {settings.min_results_for_answer})",
                "confidence": confidence,
            }
        if confidence["top_score"] < settings.min_top_score_for_answer:
            return {
                "action": "refuse",
                "reason": f"Top score too weak ({confidence['top_score']:.2f} < {settings.min_top_score_for_answer})",
                "confidence": confidence,
            }
        if confidence["avg_score"] < settings.min_avg_score_for_answer:
            return {
                "action": "refuse",
                "reason": f"Average score too weak ({confidence['avg_score']:.2f} < {settings.min_avg_score_for_answer})",
                "confidence": confidence,
            }
    
    return {
        "action": "answer",
        "reason": "Retrieved context is sufficient.",
        "confidence": confidence,
    }
