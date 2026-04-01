from __future__ import annotations
from fastapi import FastAPI, HTTPException
from git_day_practice.schema import RagRequest, RagResponse
from git_day_practice.rag import answer_with_rag

app = FastAPI(title="RAG API")

@app.get("/")
def root():
    return {"message": "RAG API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/rag", response_model=RagResponse)
def rag(payload: RagRequest):
    try:
        result = answer_with_rag(payload.question, payload.limit)
        return RagResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
