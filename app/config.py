import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Only load .env file locally, not on Railway
if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv()
    logger.info("Local environment: Loading from .env file")
else:
    logger.info("Railway environment detected")

# MongoDB settings with better fallback
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "beyou_db")

# Log configuration values (without credentials)
if MONGODB_URL:
    # Hide password in logs
    safe_url = MONGODB_URL
    if "@" in safe_url:
        parts = safe_url.split("@")
        user_pass = parts[0].split("://")[1].split(":")
        if len(user_pass) > 1:
            masked_url = f"{parts[0].split('://')[0]}://{user_pass[0]}:****@{parts[1]}"
            safe_url = masked_url
    
    logger.info(f"MongoDB connection configured with URL: {safe_url}")
    logger.info(f"Database name: {DB_NAME}")
else:
    logger.error("MONGODB_URL environment variable is not set!")