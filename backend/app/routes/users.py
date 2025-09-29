from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.database import users_collection
from app.utils import hash_password, verify_password
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from app.auth import get_current_user, role_required

# Load environment
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

# -------------------------
# Schemas
# -------------------------
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    fuel_card_no: str
    role: str = "employee"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    fuel_card_no: Optional[str] = None

class AdminUpdateUserRequest(BaseModel):
    name: Optional[str] = None
    fuel_card_no: Optional[str] = None
    role: Optional[str] = None   # only admin can set roles

# -------------------------
# Register
# -------------------------
@router.post("/register")
async def register_user(req: RegisterRequest):
    existing = await users_collection.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = {
        "name": req.name,
        "email": req.email,
        "password": hash_password(req.password),
        "fuel_card_no": req.fuel_card_no,
        "role": req.role,
        "created_at": datetime.utcnow()
    }
    result = await users_collection.insert_one(user)
    return {"msg": "User registered successfully", "id": str(result.inserted_id)}

# -------------------------
# Login
# -------------------------
@router.post("/login", response_model=TokenResponse)
async def login_user(req: LoginRequest):
    user = await users_collection.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    to_encode = {
        "sub": user["email"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# -------------------------
# Get Current User Profile
# -------------------------
@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    db_user = await users_collection.find_one({"email": user["sub"]}, {"_id": 0, "password": 0})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# -------------------------
# Update My Profile
# -------------------------
@router.put("/me")
async def update_profile(req: UpdateProfileRequest, user=Depends(get_current_user)):
    update_data = {k: v for k, v in req.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No changes provided")

    result = await users_collection.update_one(
        {"email": user["sub"]},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes applied")

    return {"msg": "✅ Profile updated successfully"}

# -------------------------
# Admin: Get All Users
# -------------------------
@router.get("/all")
async def get_all_users(user=Depends(role_required("admin"))):
    users = await users_collection.find({}, {"_id": 0, "password": 0}).to_list(1000)
    return users

# -------------------------
# Admin: Update User
# -------------------------
@router.put("/{email}")
async def admin_update_user(email: str, req: AdminUpdateUserRequest, user=Depends(role_required("admin"))):
    update_data = {k: v for k, v in req.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No changes provided")

    result = await users_collection.update_one(
        {"email": email},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"msg": f"✅ User {email} updated successfully"}

# -------------------------
# Admin: Delete User
# -------------------------
@router.delete("/{email}")
async def delete_user(email: str, user=Depends(role_required("admin"))):
    # prevent self-delete
    if email == user["sub"]:
        raise HTTPException(status_code=403, detail="Admins cannot delete themselves")

    result = await users_collection.delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"msg": f"🗑️ User {email} deleted successfully"}
