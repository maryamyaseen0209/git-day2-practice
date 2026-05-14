FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn
EXPOSE 8000
CMD ["uvicorn", "git_day_practice.simple_api:app", "--host", "0.0.0.0", "--port", "8000"]
