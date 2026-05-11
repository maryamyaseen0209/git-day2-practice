from __future__ import annotations
from sqlalchemy.orm import Session
from git_day_practice.models import RagLog
# Add to existing file
from git_day_practice.models import AgentLog

def create_agent_log(
    db: Session,
    *,
    question: str,
    normalized_query: str,
    plan: str,
    action: str,
    reason: str,
    answer: str,
) -> AgentLog:
    """Create a log entry for agent decision."""
    log = AgentLog(
        question=question,
        normalized_query=normalized_query,
        plan=plan,
        action=action,
        reason=reason,
        answer=answer,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def create_rag_log(
    db: Session,
    *,
    question: str,
    normalized_query: str,
    action: str,
    reason: str,
    answer: str,
    top_score: float,
    avg_score: float,
    result_count: int,
) -> RagLog:
    log = RagLog(
        question=question,
        normalized_query=normalized_query,
        action=action,
        reason=reason,
        answer=answer,
        top_score=top_score,
        avg_score=avg_score,
        result_count=result_count,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
