import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import sys
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Initialize client and db as None in case connection fails
client = None
db = None

# Hardcoded MongoDB connection (only for Railway deployment)
if os.getenv("RAILWAY_ENVIRONMENT") == "production":
    MONGODB_URL = "mongodb+srv://singhrishabh1670:020502@beyou.4anrb.mongodb.net/?retryWrites=true&w=majority&ssl=true&authSource=admin"
    DB_NAME = "beyou_db"
    logger.info("Using hardcoded MongoDB connection for Railway")
else:
    # For local development, use config
    from .config import MONGODB_URL, DB_NAME

try:
    # Attempt to connect to MongoDB
    if MONGODB_URL:
        logger.info(f"Attempting to connect to MongoDB database: {DB_NAME}")
        
        # Create client connection
        client = AsyncIOMotorClient(
            MONGODB_URL,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            tlsAllowInvalidCertificates=True
        )
        
        # Initialize database
        db = client[DB_NAME]
        
        logger.info("MongoDB client initialized")
    else:
        logger.warning("MONGODB_URL not set - database functionality will not be available")
        
except Exception as e:
    logger.error(f"Failed to initialize MongoDB client: {str(e)}")
    # Continue without database - API can still serve the root endpoint