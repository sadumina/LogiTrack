from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.database import users_collection
from app.utils import hash_password, verify_password
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from app.auth import get_current_user

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

# -------------------------
# Register
# -------------------------
@router.post("/register")
async def register_user(req: RegisterRequest):
    # check if email already exists
    existing = await users_collection.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = {
        "name": req.name,
        "email": req.email,
        "password": hash_password(req.password),  # hashed password
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
    # find user in DB
    user = await users_collection.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # create JWT token
    to_encode = {
        "sub": user["email"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

# -------------------------
# Get Current User Profile
# -------------------------
@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {
        "email": user["sub"],
        "role": user["role"]
    }
