FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1         PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (build + runtime)
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential curl ca-certificates         && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY backend /app/backend
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
