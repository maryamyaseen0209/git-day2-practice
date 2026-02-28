from __future__ import annotations

from typing import Annotated, Dict, List

from fastapi import FastAPI, Header, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import settings
from .settings import get_settings

# Initialize FastAPI app
app = FastAPI(title="Week 1 Day 4 - FastAPI Basics")


# ---------- PYDANTIC MODELS (Data Validation) ----------
class ItemCreate(BaseModel):
    """Model for creating an item - validates incoming data"""

    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    in_stock: bool = True


class ItemOut(BaseModel):
    """Model for returning item data - what client sees"""

    id: int
    name: str
    price: float
    in_stock: bool


class DivideRequest(BaseModel):
    """Model for division endpoint"""

    a: float
    b: float


class DivideResponse(BaseModel):
    """Model for division result"""

    result: float


class ErrorResponse(BaseModel):
    """Consistent error response format"""

    error_type: str
    message: str
    details: list[dict] | None = None


# ---------- IN-MEMORY DATABASE ----------
items: Dict[int, ItemOut] = {}
_next_id = 1


# ---------- ERROR HANDLING ----------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc: RequestValidationError):
    """Custom handler for validation errors - returns 400 with details"""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error_type="validation_error",
            message="Request data is invalid",
            details=exc.errors(),
        ).model_dump(),
    )


# ---------- CONFIGURATION ENDPOINT ----------
@app.get("/config")
async def get_config():
    """Return non-sensitive configuration"""
    settings = get_settings()
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        # Explicitly NOT returning API_KEY
    }


# ---------- SECURE ENDPOINT ----------
@app.get("/secure-data")
async def get_secure_data(x_api_key: Annotated[str | None, Header()] = None):
    """Return secure data only if valid API key provided"""
    settings = get_settings()

    if not x_api_key or x_api_key != settings.api_key:  # <-- FIXED: lowercase api_key
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {"secret_data": "approved"}


@app.get("/debug-api-key")
async def debug_api_key():
    """Debug endpoint to check API key loading"""
    settings = get_settings()

    # Get all attributes that might contain the API key
    attrs = {
        "api_key": getattr(settings, "api_key", "NOT FOUND"),
        "API_KEY": getattr(settings, "API_KEY", "NOT FOUND"),
        "ApiKey": getattr(settings, "ApiKey", "NOT FOUND"),
    }

    # Also check what environment variables are available
    import os

    env_vars = {
        "API_KEY": os.environ.get("API_KEY", "NOT SET"),
        "API_KEY_FROM_ENV": os.environ.get("API_KEY", "NOT SET"),
    }

    # Check all attributes of settings
    all_attrs = [attr for attr in dir(settings) if not attr.startswith("_")]

    return {
        "settings_attributes": attrs,
        "environment_variables": env_vars,
        "all_attributes": all_attrs,
        "settings_type": str(type(settings)),
    }


# ---------- ROUTES (API Endpoints) ----------
@app.get("/health")
async def health():
    """Health check endpoint"""
    settings = get_settings()
    # Safe access to settings attributes
    return {
        "status": "healthy",
        "app_name": getattr(settings, "APP_NAME", "Unknown"),
        "environment": getattr(settings, "ENVIRONMENT", "unknown"),
        "debug": getattr(settings, "debug", False),
    }


@app.post("/items", response_model=ItemOut, status_code=201)
async def create_item(payload: ItemCreate):
    """Create a new item"""
    global _next_id
    item = ItemOut(id=_next_id, **payload.model_dump())
    items[_next_id] = item
    _next_id += 1
    return item


@app.get("/items", response_model=List[ItemOut])
async def list_items():
    """List all items"""
    return list(items.values())


@app.get("/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item by ID"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return None


@app.post("/math/divide", response_model=DivideResponse)
async def divide(payload: DivideRequest):
    """Divide two numbers"""
    if payload.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return DivideResponse(result=payload.a / payload.b)
