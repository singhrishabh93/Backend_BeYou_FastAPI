import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME, logger
import os

# Check if MongoDB URL is provided
if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is not set")

logger.info("Attempting to connect to MongoDB...")

try:
    # For Railway deployment - with better error handling
    client = AsyncIOMotorClient(
        MONGODB_URL,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        tlsAllowInvalidCertificates=True
    )
    
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
    
    db = client[DB_NAME]
    
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise