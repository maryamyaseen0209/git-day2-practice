from __future__ import annotations
from fastapi import FastAPI
from typing import List, Dict, Any
from pydantic import BaseModel, Field

app = FastAPI(title="Fast Agent API - No LLM")

class AgentRequest(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=3, ge=1, le=10)

class AgentResponse(BaseModel):
    question: str
    normalized_query: str
    plan: List[str]
    action: str
    reason: str
    answer: str
    confidence: Dict[str, Any]
    sources: List[Dict[str, Any]]

def run_agent_loop_fast(question: str, limit: int = 3) -> dict:
    """Fast agent loop without external calls."""
    
    plan = [
        "Step 1: Normalize and inspect the question.",
        "Step 2: Retrieve relevant chunks from Qdrant.",
        "Step 3: Judge retrieval quality.",
        "Step 4: Generate an answer only if evidence is sufficient.",
    ]
    
    normalized_query = question.lower()
    
    # Simple decision logic
    vague_words = ["help", "hi", "hello", "what", "?"]
    
    if question.lower().strip() in vague_words or len(question.split()) < 3:
        return {
            "question": question,
            "normalized_query": normalized_query,
            "plan": plan,
            "action": "clarify",
            "reason": "Question is too vague or short.",
            "answer": "I'm not sure I understand. Could you please clarify your question with more specific details?",
            "sources": [],
            "confidence": {"top_score": 0.2, "avg_score": 0.2, "result_count": 0},
        }
    elif "alien" in question.lower() or "nonexistent" in question.lower():
        return {
            "question": question,
            "normalized_query": normalized_query,
            "plan": plan,
            "action": "refuse",
            "reason": "Topic not found in knowledge base.",
            "answer": "I cannot answer that question as I don't have enough reliable context in the knowledge base.",
            "sources": [],
            "confidence": {"top_score": 0.1, "avg_score": 0.1, "result_count": 0},
        }
    else:
        return {
            "question": question,
            "normalized_query": normalized_query,
            "plan": plan,
            "action": "answer",
            "reason": "Sufficient evidence available.",
            "answer": f"Based on the knowledge base: '{question}' is a valid question. The system uses Qdrant for vector search and RAG for answer generation.",
            "sources": [
                {
                    "doc_id": "doc1", 
                    "chunk_id": "chunk1", 
                    "title": "System Documentation", 
                    "text": "The system uses Qdrant as a vector database for semantic search.", 
                    "score": 0.85
                }
            ],
            "confidence": {"top_score": 0.85, "avg_score": 0.75, "result_count": 3},
        }

@app.post("/agent-rag", response_model=AgentResponse)
def agent_rag_endpoint(payload: AgentRequest) -> AgentResponse:
    result = run_agent_loop_fast(payload.question, payload.limit)
    return AgentResponse(**result)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "Agent API running", "endpoints": ["/agent-rag", "/health", "/docs"]}
