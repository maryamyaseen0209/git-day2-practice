from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sys

sys.path.insert(0, '/app/src')

app = FastAPI(title="Working API")

@app.get("/health")
def health():
    return {"status": "healthy", "agent_enabled": True}

@app.get("/health/ready")
def ready():
    return {"status": "ready"}

@app.post("/rag")
async def rag(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "")
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
        return {
            "question": question,
            "answer": f"Agent response for: {question}",
            "steps": 3,
            "status": "success"
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

