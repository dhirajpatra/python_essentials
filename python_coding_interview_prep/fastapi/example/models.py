# models.py
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pymongo.database import Database


def serialize_user(doc: dict) -> dict:
    """Convert MongoDB doc → JSON-friendly dict."""
    if not doc:
        return {}
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "age": doc.get("age"),
        "created_at": doc.get("created_at"),
    }


def parse_object_id(value: str) -> Optional[ObjectId]:
    """Safe ObjectId parsing — returns None if invalid."""
    try:
        return ObjectId(value)
    except Exception:
        return None


def create_user_doc(name: str, email: str, age: Optional[int]) -> dict:
    return {
        "name": name,
        "email": email,
        "age": age,
        "created_at": datetime.utcnow(),
    }