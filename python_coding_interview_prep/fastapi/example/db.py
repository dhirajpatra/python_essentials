# db.py
import os
from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "myapp")

# Create ONE client for the whole app (thread-safe, connection-pooled)
client: MongoClient = MongoClient(
    MONGO_URI,
    maxPoolSize=50,          # connection pool size
    minPoolSize=5,
    serverSelectionTimeoutMS=5000,
    uuidRepresentation="standard",
)

db: Database = client[DB_NAME]

# # db.py (async version)
# from motor.motor_asyncio import AsyncIOMotorClient
#
# client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = client["myapp"]
#
# async def get_db():
#     return db


def get_db() -> Database:
    """Dependency for FastAPI routes."""
    return db


def init_indexes() -> None:
    """Create indexes on startup."""
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.users.create_index([("name", ASCENDING)])