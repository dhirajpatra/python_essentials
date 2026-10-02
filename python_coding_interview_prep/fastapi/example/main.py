# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from db import client, init_indexes
from routes import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_indexes()
    # sanity check
    client.admin.command("ping")
    print("✅ Connected to MongoDB")
    yield
    # shutdown
    client.close()
    print("🔌 MongoDB connection closed")


app = FastAPI(title="FastAPI + PyMongo", lifespan=lifespan)
app.include_router(users_router)


@app.get("/health")
def health():
    return {"status": "ok"}