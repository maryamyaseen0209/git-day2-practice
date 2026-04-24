# from __future__ import annotations
# from fastapi import FastAPI, HTTPException
# from git_day_practice.schema import RagRequest, RagResponse
# from git_day_practice.rag import answer_with_rag

# app = FastAPI(title="RAG API")


# @app.get("/")
# def root():
#     return {"message": "RAG API is running"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# @app.post("/rag", response_model=RagResponse)
# def rag(payload: RagRequest):
#     try:
#         result = answer_with_rag(payload.question, payload.limit)
#         return RagResponse(
#             question=result["question"],
#             answer=result["answer"],
#             sources=result["sources"]
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# from __future__ import annotations
# from fastapi import FastAPI, HTTPException
# from git_day_practice.rag import answer_with_rag
# from git_day_practice.schema import RagRequest, RagResponse

# app = FastAPI(title="AI Retrieval and RAG API")

# @app.post("/rag", response_model=RagResponse)
# def rag_endpoint(payload: RagRequest) -> RagResponse:
#     try:
#         result = answer_with_rag(payload.question, payload.limit)
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"RAG failed: {exc}") from exc
    
#     return RagResponse(
#         question=result["question"],
#         normalized_query=result["normalized_query"],
#         answer=result["answer"],
#         sources=result["sources"],
#     )

from __future__ import annotations
from fastapi import FastAPI, HTTPException
from git_day_practice.schema import RagRequest, RagResponse
from git_day_practice.normalization import normalize_roman_urdu

# Use mock retrieval - no Qdrant needed!
from git_day_practice.retrieval_mock import dual_query_search_mock

app = FastAPI(title="AI Retrieval and RAG API")

@app.get("/")
def root():
    return {"message": "RAG API is running", "status": "healthy"}

@app.post("/rag", response_model=RagResponse)
def rag_endpoint(payload: RagRequest) -> RagResponse:
    try:
        # Use mock retrieval (doesn't need Qdrant)
        result = dual_query_search_mock(payload.question, payload.limit)
        
        # Create answer from retrieved chunks
        if result["results"]:
            answer = f"Based on the retrieved context: {result['results'][0]['text']}"
        else:
            answer = "No relevant documents found for your question."
        
        return RagResponse(
            question=result["original_query"],
            normalized_query=result["normalized_query"],
            answer=answer,
            sources=result["results"],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG failed: {exc}") from exc
