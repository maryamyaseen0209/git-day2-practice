from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI, Header, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .settings import get_settings  # Import settings (relative import)

# Load settings
settings = get_settings()

# Initialize FastAPI app with settings
app = FastAPI(title=settings.app_name)

# ---------- PYDANTIC MODELS (Data Validation) ----------
# These define the shape of data our API accepts/returns


class ItemCreate(BaseModel):
    """Model for creating an item - validates incoming data"""

    name: str = Field(min_length=1, max_length=50)  # name must be 1-50 chars
    price: float = Field(gt=0)  # price must be > 0
    in_stock: bool = True  # optional, defaults to True


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
# Simple dictionary to store items (instead of real database)
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


# ---------- CONFIGURATION ENDPOINT (NEW for Day 5) ----------
@app.get("/config")
async def show_config():
    """Show non-sensitive configuration (Day 5 feature)"""
    s = get_settings()
    return {
        "app_name": s.app_name,
        "environment": s.environment,
        "debug": s.debug,
        "host": s.host,
        "port": s.port,
        "allowed_origins": s.allowed_origins,
    }


# ---------- SECURE ENDPOINT (NEW for Day 5) ----------
@app.get("/secure-data")
async def secure_data(x_api_key: str | None = Header(default=None)):
    """Secure endpoint that requires API key (Day 5 feature)"""
    s = get_settings()
    if x_api_key != s.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"secret_data": "approved", "message": "You have access to secure data!"}


# ---------- ROUTES (API Endpoints from Day 4) ----------
@app.get("/health")
async def health():
    """Simple health check endpoint"""
    return {"status": "healthy", "environment": settings.environment}


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
