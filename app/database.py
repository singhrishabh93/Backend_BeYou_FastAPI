import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME
import os

# Fix the MongoDB URL format
corrected_url = MONGODB_URL
if "mongodb+srv://" in MONGODB_URL and "retryWrites=true" in MONGODB_URL:
    # Parse and fix the URL format
    parts = MONGODB_URL.split('@')
    if len(parts) == 2:
        credentials = parts[0]
        hostname_and_params = parts[1].split('/')
        
        if len(hostname_and_params) >= 1:
            hostname = hostname_and_params[0]
            # Reconstruct with proper formatting
            corrected_url = f"{credentials}@{hostname}/?retryWrites=true&w=majority&ssl=true&authSource=admin"

# Log connection info (during development only)
if not os.getenv("RAILWAY_ENVIRONMENT"):
    print(f"Using MongoDB URL: {corrected_url}")

# For Railway deployment
client = AsyncIOMotorClient(
    corrected_url,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=20000,  # Increased timeout
    connectTimeoutMS=30000,
    socketTimeoutMS=30000,
    tlsAllowInvalidCertificates=True
)
db = client[DB_NAME]