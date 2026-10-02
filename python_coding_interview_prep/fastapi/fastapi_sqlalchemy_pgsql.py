# main.py
from contextlib import asynccontextmanager
from typing import Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, Integer, DateTime, select
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ---------- SQLAlchemy setup ----------
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/myapp"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


# ---------- Pydantic schemas ----------
class UserIn(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: datetime


# ---------- FastAPI app ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.get("/users", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()


@app.get("/users/search", response_model=List[UserOut])
async def search_users(min_age: int = 0, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.age >= min_age))
    return result.scalars().all()


@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=UserOut)
async def create_user(payload: UserIn, db: AsyncSession = Depends(get_db)):
    user = User(**payload.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user