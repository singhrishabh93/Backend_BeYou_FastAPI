from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import sys

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Print environment variables for debugging (except sensitive ones)
for key, value in os.environ.items():
    if not any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token']):
        logger.info(f"ENV: {key}={value}")

app = FastAPI(
    title="BeYou API",
    description="API for BeYou affirmations",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint used for healthcheck"""
    logger.info("Health check endpoint called")
    return {"message": "Welcome to BeYou API", "status": "online"}

# Try to load other routes only if this basic app works
try:
    from .models.routers import affirmation
    app.include_router(affirmation.router)
    logger.info("Successfully loaded affirmation router")
except Exception as e:
    logger.error(f"Failed to load affirmation router: {str(e)}")
    # Continue running even if router loading fails
    pass