# Run this to patch the health endpoint
import docker

client = docker.from_env()
container = client.containers.get('git-day2-practice-api-1')
exec_result = container.exec_run([
    "python", "-c", """
import sys
sys.path.insert(0, '/app/src')
with open('/app/src/git_day_practice/api.py', 'r') as f:
    content = f.read()

# Replace the problematic health endpoint
old_health = '''@app.get("/health/ready")
def ready_health() -> dict[str, str]:
    try:
        with pyscopy.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                - = cur.fetchone()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"postgres not ready: {exc}") from exc

    try: client = QdrantClient(url=settings.qdrant_url)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"qdrant not ready: {exc}") from exc
    return {"status": "ready"}'''

new_health = '''@app.get("/health/ready")
def ready_health() -> dict[str, str]:
    try:
        with psycopg2.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"postgres not ready: {exc}") from exc
    
    # Check Qdrant using the correct attribute
    try:
        qdrant_url = getattr(settings, 'qdrant_url', 'http://qdrant:6333')
        client = QdrantClient(url=qdrant_url)
        client.get_collections()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"qdrant not ready: {exc}") from exc
    return {"status": "ready"}'''

content = content.replace(old_health, new_health)
with open('/app/src/git_day_practice/api.py', 'w') as f:
    f.write(content)
print("Health endpoint fixed")
"""
])
print(exec_result.output.decode())
