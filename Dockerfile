FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add curl for health check
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start application with PORT environment variable
CMD echo "Starting app on port $PORT" && uvicorn app.main:app --host 0.0.0.0 --port $PORT