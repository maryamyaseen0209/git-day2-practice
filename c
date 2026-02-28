[1mdiff --git a/.dockerignore b/.dockerignore[m
[1mindex 6200d3e..9826793 100644[m
[1m--- a/.dockerignore[m
[1m+++ b/.dockerignore[m
[36m@@ -15,4 +15,4 @@[m [m__pycache__/[m
 # Test / tooling caches[m
 .pytest_cache/[m
 .ruff_cache/[m
[31m-.mypy_cache/[m
\ No newline at end of file[m
[32m+[m[32m.mypy_cache/[m
[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex 2c66a37..1d5abad 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -22,4 +22,4 @@[m [mbuild/[m
 .vscode/[m
 .idea/[m
 *.swp[m
[31m-*.swo[m
\ No newline at end of file[m
[32m+[m[32m*.swo[m
[1mdiff --git a/Dockerfile b/Dockerfile[m
[1mindex 57cd05a..ebc9d49 100644[m
[1m--- a/Dockerfile[m
[1m+++ b/Dockerfile[m
[36m@@ -18,4 +18,4 @@[m [mRUN python -m pip install --upgrade pip \[m
 EXPOSE 8000[m
 [m
 # Start the API - CORRECTED PATH to your app[m
[31m-CMD ["uvicorn", "src.git_day_practice.api:app", "--host", "0.0.0.0", "--port", "8000"][m
\ No newline at end of file[m
[32m+[m[32mCMD ["uvicorn", "src.git_day_practice.api:app", "--host", "0.0.0.0", "--port", "8000"][m
[1mdiff --git a/src/git_day_practice/api.py b/src/git_day_practice/api.py[m
[1mindex 2dc7a34..0204f19 100644[m
[1m--- a/src/git_day_practice/api.py[m
[1m+++ b/src/git_day_practice/api.py[m
[36m@@ -1,49 +1,63 @@[m
 from __future__ import annotations[m
[31m-from typing import Dict, List, Annotated[m
[31m-from fastapi import FastAPI, HTTPException, Header[m
[32m+[m
[32m+[m[32mfrom typing import Annotated, Dict, List[m
[32m+[m
[32m+[m[32mfrom fastapi import FastAPI, Header, HTTPException[m
 from fastapi.exceptions import RequestValidationError[m
 from fastapi.responses import JSONResponse[m
 from pydantic import BaseModel, Field[m
 [m
 # Import settings[m
[31m-from .settings import get_settings, Settings[m
[32m+[m[32mfrom .settings import get_settings[m
 [m
 # Initialize FastAPI app[m
 app = FastAPI(title="Week 1 Day 4 - FastAPI Basics")[m
 [m
[32m+[m
 # ---------- PYDANTIC MODELS (Data Validation) ----------[m
 class ItemCreate(BaseModel):[m
     """Model for creating an item - validates incoming data"""[m
[32m+[m
     name: str = Field(min_length=1, max_length=50)[m
     price: float = Field(gt=0)[m
     in_stock: bool = True[m
 [m
[32m+[m
 class ItemOut(BaseModel):[m
     """Model for returning item data - what client sees"""[m
[32m+[m
     id: int[m
     name: str[m
     price: float[m
     in_stock: bool[m
 [m
[32m+[m
 class DivideRequest(BaseModel):[m
     """Model for division endpoint"""[m
[32m+[m
     a: float[m
     b: float[m
 [m
[32m+[m
 class DivideResponse(BaseModel):[m
     """Model for division result"""[m
[32m+[m
     result: float[m
 [m
[32m+[m
 class ErrorResponse(BaseModel):[m
     """Consistent error response format"""[m
[32m+[m
     error_type: str[m
     message: str[m
     details: list[dict] | None = None[m
 [m
[32m+[m
 # ---------- IN-MEMORY DATABASE ----------[m
 items: Dict[int, ItemOut] = {}[m
 _next_id = 1[m
 [m
[32m+[m
 # ---------- ERROR HANDLING ----------[m
 @app.exception_handler(RequestValidationError)[m
 async def validation_exception_handler(_request, exc: RequestValidationError):[m
[36m@@ -57,6 +71,7 @@[m [masync def validation_exception_handler(_request, exc: RequestValidationError):[m
         ).model_dump(),[m
     )[m
 [m
[32m+[m
 # ---------- CONFIGURATION ENDPOINT ----------[m
 @app.get("/config")[m
 async def get_config():[m
[36m@@ -64,27 +79,67 @@[m [masync def get_config():[m
     settings = get_settings()[m
     return {[m
         "app_name": settings.APP_NAME,[m
[31m-        "environment": settings.ENVIRONMENT[m
[32m+[m[32m        "environment": settings.ENVIRONMENT,[m
         # Explicitly NOT returning API_KEY[m
     }[m
 [m
[32m+[m
 # ---------- SECURE ENDPOINT ----------[m
 @app.get("/secure-data")[m
 async def get_secure_data(x_api_key: Annotated[str | None, Header()] = None):[m
     """Return secure data only if valid API key provided"""[m
     settings = get_settings()[m
[31m-    [m
[31m-    if not x_api_key or x_api_key != settings.API_KEY:[m
[32m+[m
[32m+[m[32m    if not x_api_key or x_api_key != settings.api_key:  # <-- FIXED: lowercase api_key[m
         raise HTTPException(status_code=401, detail="Invalid API Key")[m
[31m-    [m
[32m+[m
     return {"secret_data": "approved"}[m
 [m
[32m+[m
[32m+[m[32m@app.get("/debug-api-key")[m
[32m+[m[32masync def debug_api_key():[m
[32m+[m[32m    """Debug endpoint to check API key loading"""[m
[32m+[m[32m    settings = get_settings()[m
[32m+[m
[32m+[m[32m    # Get all attributes that might contain the API key[m
[32m+[m[32m    attrs = {[m
[32m+[m[32m        "api_key": getattr(settings, "api_key", "NOT FOUND"),[m
[32m+[m[32m        "API_KEY": getattr(settings, "API_KEY", "NOT FOUND"),[m
[32m+[m[32m        "ApiKey": getattr(settings, "ApiKey", "NOT FOUND"),[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    # Also check what environment variables are available[m
[32m+[m[32m    import os[m
[32m+[m
[32m+[m[32m    env_vars = {[m
[32m+[m[32m        "API_KEY": os.environ.get("API_KEY", "NOT SET"),[m
[32m+[m[32m        "API_KEY_FROM_ENV": os.environ.get("API_KEY", "NOT SET"),[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    # Check all attributes of settings[m
[32m+[m[32m    all_attrs = [attr for attr in dir(settings) if not attr.startswith("_")][m
[32m+[m
[32m+[m[32m    return {[m
[32m+[m[32m        "settings_attributes": attrs,[m
[32m+[m[32m        "environment_variables": env_vars,[m
[32m+[m[32m        "all_attributes": all_attrs,[m
[32m+[m[32m        "settings_type": str(type(settings)),[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m
 # ---------- ROUTES (API Endpoints) ----------[m
 @app.get("/health")[m
 async def health():[m
[31m-    """Simple health check endpoint"""[m
[32m+[m[32m    """Health check endpoint"""[m
     settings = get_settings()[m
[31m-    return {"status": "healthy", "environment": settings.ENVIRONMENT}[m
[32m+[m[32m    # Safe access to settings attributes[m
[32m+[m[32m    return {[m
[32m+[m[32m        "status": "healthy",[m
[32m+[m[32m        "app_name": getattr(settings, "APP_NAME", "Unknown"),[m
[32m+[m[32m        "environment": getattr(settings, "ENVIRONMENT", "unknown"),[m
[32m+[m[32m        "debug": getattr(settings, "debug", False),[m
[32m+[m[32m    }[m
[32m+[m
 [m
 @app.post("/items", response_model=ItemOut, status_code=201)[m
 async def create_item(payload: ItemCreate):[m
[36m@@ -95,11 +150,13 @@[m [masync def create_item(payload: ItemCreate):[m
     _next_id += 1[m
     return item[m
 [m
[32m+[m
 @app.get("/items", response_model=List[ItemOut])[m
 async def list_items():[m
     """List all items"""[m
     return list(items.values())[m
 [m
[32m+[m
 @app.get("/items/{item_id}", response_model=ItemOut)[m
 async def get_item(item_id: int):[m
     """Get a specific item by ID"""[m
[36m@@ -107,6 +164,7 @@[m [masync def get_item(item_id: int):[m
         raise HTTPException(status_code=404, detail="Item not found")[m
     return items[item_id][m
 [m
[32m+[m
 @app.delete("/items/{item_id}", status_code=204)[m
 async def delete_item(item_id: int):[m
     """Delete an item by ID"""[m
[36m@@ -115,9 +173,10 @@[m [masync def delete_item(item_id: int):[m
     del items[item_id][m
     return None[m
 [m
[32m+[m
 @app.post("/math/divide", response_model=DivideResponse)[m
 async def divide(payload: DivideRequest):[m
     """Divide two numbers"""[m
     if payload.b == 0:[m
         raise HTTPException(status_code=400, detail="Division by zero is not allowed")[m
[31m-    return DivideResponse(result=payload.a / payload.b)[m
\ No newline at end of file[m
[32m+[m[32m    return DivideResponse(result=payload.a / payload.b)[m
[1mdiff --git a/src/git_day_practice/settings.py b/src/git_day_practice/settings.py[m
[1mindex 3540082..d92cd8d 100644[m
[1m--- a/src/git_day_practice/settings.py[m
[1m+++ b/src/git_day_prac
