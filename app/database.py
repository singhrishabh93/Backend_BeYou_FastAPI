import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME

# For Railway deployment
client = AsyncIOMotorClient(
    MONGODB_URL,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)
db = client[DB_NAME]