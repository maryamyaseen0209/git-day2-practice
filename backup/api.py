from __future__ import annotations

from fastapi import FastAPI, HTTPException
from git_day_practice.schema import RagRequest, RagResponse
from git_day_practice.rag import answer_with_rag

# Create FastAPI app
app = FastAPI(title="RAG API")

@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "RAG API is running"}

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/rag", response_model=RagResponse)
def rag_endpoint(payload: RagRequest):
    """
    RAG endpoint that retrieves context and generates an answer.
    
    - **question**: User's question (minimum 1 character)
    - **limit**: Number of chunks to retrieve (1-10, default: 3)
    
    Returns:
        - Generated answer with citations
        - Retrieved source chunks with metadata
    """
    try:
        result = answer_with_rag(payload.question, payload.limit)
        return RagResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500, 
            detail=f"RAG processing failed: {str(exc)}"
        ) from exc