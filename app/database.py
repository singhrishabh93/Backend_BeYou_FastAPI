import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME
import logging
import sys

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