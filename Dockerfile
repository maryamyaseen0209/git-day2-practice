# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Good defaults for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project files
COPY . /app

# Install runtime deps
RUN python -m pip install --upgrade pip && \
    python -m pip install "fastapi[standard]" pydantic-settings "psycopg[binary]" qdrant-client

# Expose the port your API will listen on
EXPOSE 8000

# Start the API - CORRECTED PATH to your app
CMD ["uvicorn", "src.git_day_practice.api:app", "--host", "0.0.0.0", "--port", "8000"]
