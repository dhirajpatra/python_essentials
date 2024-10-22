from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserResponse
from database import database
import bcrypt

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    query = select(User).where(User.email == user.email)
    existing_user = await database.fetch_one(query)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name=user.name, email=user.email, password=hashed_password.decode('utf-8'))
    
    query = User.__table__.insert().values(name=user.name, email=user.email, password=new_user.password)
    await database.execute(query)
    
    return new_user

@router.post("/login")
async def login_user(user: UserCreate):
    query = select(User).where(User.email == user.email)
    existing_user = await database.fetch_one(query)

    if not existing_user or not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful"}
