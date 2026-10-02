# routes.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from db import get_db
from models import serialize_user, parse_object_id, create_user_doc
from schemas import UserIn, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

# # routes.py (async version)
# @router.get("", response_model=List[UserOut])
# async def list_users(db = Depends(get_db)):
#     cursor = db.users.find({}).limit(20)
#     return [serialize_user(d) async for d in cursor]  # note: async for

# ---------- CREATE ----------
@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserIn, db: Database = Depends(get_db)):
    doc = create_user_doc(payload.name, payload.email, payload.age)
    try:
        result = db.users.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(409, "Email already exists")

    doc["_id"] = result.inserted_id
    return serialize_user(doc)


# ---------- READ (list + filter + pagination) ----------
@router.get("", response_model=List[UserOut])
def list_users(
    min_age: Optional[int] = Query(None, ge=0),
    name_contains: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Database = Depends(get_db),
):
    query = {}
    if min_age is not None:
        query["age"] = {"$gte": min_age}
    if name_contains:
        query["name"] = {"$regex": name_contains, "$options": "i"}

    cursor = db.users.find(query).skip(skip).limit(limit).sort("created_at", -1)
    return [serialize_user(d) for d in cursor]


# ---------- READ (single) ----------
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Database = Depends(get_db)):
    oid = parse_object_id(user_id)
    if oid is None:
        raise HTTPException(400, "Invalid user id")

    doc = db.users.find_one({"_id": oid})
    if not doc:
        raise HTTPException(404, "User not found")
    return serialize_user(doc)


# ---------- UPDATE ----------
@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: str, payload: UserUpdate, db: Database = Depends(get_db)):
    oid = parse_object_id(user_id)
    if oid is None:
        raise HTTPException(400, "Invalid user id")

    updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not updates:
        raise HTTPException(400, "No fields to update")

    try:
        doc = db.users.find_one_and_update(
            {"_id": oid},
            {"$set": updates},
            return_document=True,   # return the updated doc
        )
    except DuplicateKeyError:
        raise HTTPException(409, "Email already exists")

    if not doc:
        raise HTTPException(404, "User not found")
    return serialize_user(doc)


# ---------- DELETE ----------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Database = Depends(get_db)):
    oid = parse_object_id(user_id)
    if oid is None:
        raise HTTPException(400, "Invalid user id")

    result = db.users.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(404, "User not found")
    return None


# ---------- AGGREGATION EXAMPLE ----------
@router.get("/stats/by-age")
def age_stats(db: Database = Depends(get_db)):
    pipeline = [
        {"$match": {"age": {"$ne": None}}},
        {"$group": {
            "_id": None,
            "avg_age": {"$avg": "$age"},
            "min_age": {"$min": "$age"},
            "max_age": {"$max": "$age"},
            "count": {"$sum": 1},
        }},
    ]
    result = list(db.users.aggregate(pipeline))
    return result[0] if result else {"count": 0}