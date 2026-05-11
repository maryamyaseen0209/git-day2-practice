from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from git_day_practice.db import get_db
from git_day_practice.rag import answer_with_rag
from git_day_practice.guardrails import choose_rag_action
from git_day_practice.settings import settings
from git_day_practice.agent import run_agent_loop
from git_day_practice.logging_utils import create_agent_log

# Pydantic models for requests/responses
from pydantic import BaseModel, Field

class RAGRequest(BaseModel):
    question: str = Field(min_length=1, description="The user question.")
    limit: int = Field(default=3, ge=1, le=10)

class RAGResponse(BaseModel):
    question: str
    normalized_query: str
    answer: str
    sources: List[dict]

class AgentRequest(BaseModel):
    question: str = Field(min_length=1, description="The user question.")
    limit: int = Field(default=3, ge=1, le=10)

class AgentResponse(BaseModel):
    question: str
    normalized_query: str
    plan: List[str]
    action: str
    reason: str
    answer: str
    confidence: dict
    sources: List[dict]

# Create FastAPI app
app = FastAPI(
    title="AI Retrieval, RAG, and Agent API",
    description="Day 15-18: RAG with agent loop",
    version="1.0.0"
)

# Day 15: Basic RAG endpoint
@app.post("/rag", response_model=RAGResponse)
def rag_endpoint(payload: RAGRequest) -> RAGResponse:
    """Basic RAG endpoint from Day 15."""
    try:
        result = answer_with_rag(payload.question, payload.limit)
        return RAGResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG failed: {exc}")

# Day 18: Agent loop endpoint
@app.post("/agent-rag", response_model=AgentResponse)
def agent_rag_endpoint(
    payload: AgentRequest,
    db: Session = Depends(get_db)
) -> AgentResponse:
    """
    Agent-based RAG endpoint with explicit plan -> retrieve -> judge -> answer flow.
    """
    try:
        # Run the agent loop
        result = run_agent_loop(payload.question, payload.limit)
        
        # Log to database if enabled
        if settings.enable_agent_logging:
            create_agent_log(
                db,
                question=result["question"],
                normalized_query=result["normalized_query"],
                plan="\n".join(result["plan"]),
                action=result["action"],
                reason=result["reason"],
                answer=result["answer"],
            )
        
        return AgentResponse(**result)
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent RAG failed: {exc}")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "agent_enabled": settings.enable_agent_loop}

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "RAG Agent API",
        "endpoints": ["/rag", "/agent-rag", "/health", "/docs"],
        "docs": "/docs"
    }
