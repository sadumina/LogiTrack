from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.database import travels_collection
from app.auth import get_current_user

router = APIRouter()

class TravelLogRequest(BaseModel):
    date: Optional[datetime] = None
    distance: float
    type: str   # "personal" or "official"
    remarks: Optional[str] = ""

@router.post("/")
async def add_travel(log: TravelLogRequest, user=Depends(get_current_user)):
    log_data = {
        "user_id": user["sub"],
        "date": log.date or datetime.utcnow(),
        "distance": log.distance,
        "type": log.type,
        "remarks": log.remarks,
    }
    await travels_collection.insert_one(log_data)
    return {"msg": "✅ Travel log added"}

@router.get("/")
async def get_my_travels(user=Depends(get_current_user)):
    logs = await travels_collection.find({"user_id": user["sub"]}).to_list(100)
    return logs
