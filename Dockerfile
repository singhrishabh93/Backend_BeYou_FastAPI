FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add debugging for startup issues
RUN apt-get update && apt-get install -y procps iputils-ping

# Environment variables
ENV PYTHONUNBUFFERED=1

# Healthcheck
HEALTHCHECK --interval=5s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Startup script to ensure container runs properly
CMD ["sh", "-c", "echo 'Starting FastAPI app...' && uvicorn app.main:app --host 0.0.0.0 --port 8000"]