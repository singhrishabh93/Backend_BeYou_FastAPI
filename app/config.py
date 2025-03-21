import os
from dotenv import load_dotenv

# Only load .env file locally, not on Railway
if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv()

# MongoDB settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "beyou_db")