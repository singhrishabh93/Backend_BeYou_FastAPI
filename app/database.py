import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME

# For Railway deployment - with adjusted SSL settings
client = AsyncIOMotorClient(
    MONGODB_URL,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000,
    ssl=True,
    ssl_cert_reqs='CERT_NONE'  # Try this for Railway deployment
)
db = client[DB_NAME]