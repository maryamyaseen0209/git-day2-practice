from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import psycopg2
from qdrant_client import QdrantClient
import sys
import os

sys.path.insert(0, '/app/src')

from git_day_practice.settings import settings

app = FastAPI(title="AI Backend API")

@app.get("/")
def root():
    return {"message": "AI Backend API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "agent_enabled": True}

@app.get("/health/ready")
def ready_health():
    try:
        with psycopg2.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"postgres not ready: {exc}")
    
    try:
        client = QdrantClient(url=settings.qdrant_url)
        client.get_collections()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"qdrant not ready: {exc}")
    
    return {"status": "ready"}

@app.post("/rag")
async def rag_endpoint(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "")
        limit = data.get("limit", 3)
        
        return {
            "question": question,
            "answer": f"This is a working response for: {question}",
            "sources": ["mock_source_1", "mock_source_2"],
            "status": "success"
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/agent-rag")
async def agent_rag(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "")
        limit = data.get("limit", 3)
        
        return {
            "question": question,
            "answer": f"Agent response for: {question}",
            "steps": 3,
            "status": "success"
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

