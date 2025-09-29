from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.database import travels_collection
from app.auth import get_current_user, role_required

router = APIRouter()

# -------------------------
# Schemas
# -------------------------
class TravelLogRequest(BaseModel):
    date: Optional[str] = Field(None, example="2025-09-29")
    personal_km: float = 0
    official_km: float = 0
    remarks: Optional[str] = ""

# -------------------------
# Employee: Add Travel Log
# -------------------------
@router.post("/")
async def add_travel(log: TravelLogRequest, user=Depends(get_current_user)):
    if log.personal_km < 0 or log.official_km < 0:
        raise HTTPException(status_code=400, detail="Distance cannot be negative")

    log_data = {
        "user_email": user["sub"],
        "date": log.date or datetime.utcnow().strftime("%Y-%m-%d"),
        "personal_km": log.personal_km,
        "official_km": log.official_km,
        "remarks": log.remarks,
        "created_at": datetime.utcnow()
    }
    await travels_collection.insert_one(log_data)
    return {"msg": "✅ Travel log added"}

# -------------------------
# Employee: View My Logs
# -------------------------
@router.get("/me")
async def get_my_travels(user=Depends(get_current_user)):
    logs = await travels_collection.find({"user_email": user["sub"]}).to_list(500)
    return logs

# -------------------------
# Admin: View All Logs
# -------------------------
@router.get("/all")
async def get_all_travels(user=Depends(role_required("admin"))):
    logs = await travels_collection.find().to_list(5000)
    return logs
