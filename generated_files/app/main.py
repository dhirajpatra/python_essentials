from fastapi import FastAPI
from routes.auth import router as auth_router
from database import database, metadata

app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
async def startup():
    # Connect to the database
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    # Disconnect from the database
    await database.disconnect()
