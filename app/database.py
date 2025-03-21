import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if MongoDB URL is provided
if not MONGODB_URL:
    logger.error("MONGODB_URL environment variable is not set. Using localhost fallback.")
    MONGODB_URL = "mongodb://localhost:27017"

logger.info(f"Connecting to database: {DB_NAME}")

try:
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
    
    # Test connection in a non-blocking way (don't do this at import time)
    logger.info("MongoDB client initialized (connection will be tested on first request)")
    
except Exception as e:
    logger.error(f"Failed to initialize MongoDB client: {str(e)}")
    # Don't raise exception at import time - this would prevent app from starting
    db = None