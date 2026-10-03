# main.py
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime

from beanie import Document, init_beanie
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field


# 1. Define the document model (this is your "table")
class User(Document):
    name: str = Field(...)
    email: str = Field(...)
    age: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Beanie uses this to know which collection to use
    class Settings:
        name = "users"  # MongoDB collection name


# 2. Initialize Beanie during app startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client["myapp"],
        document_models=[User]
    )
    yield
    client.close()


app = FastAPI(lifespan=lifespan)


# 3. Read all users
@app.get("/users")
async def list_users():
    users = await User.find_all().to_list()
    return users


# 4. Query with a condition
@app.get("/users/search")
async def search_users(min_age: int = 0):
    users = await User.find(User.age >= min_age).to_list()
    return users


# 5. Get a single user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 6. Create a user (useful for testing)
@app.post("/users")
async def create_user(name: str, email: str, age: int = None):
    user = User(name=name, email=email, age=age)
    await user.insert()
    return user