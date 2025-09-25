import motor.motor_asyncio
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "fueltrackr")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
travels_collection = db["travels"]

# =========================
# 🔹 Helper Functions
# =========================

# Convert ObjectId → str for JSON
def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable dict"""
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

# -------------------------
# USERS
# -------------------------
async def find_user_by_email(email: str):
    user = await users_collection.find_one({"email": email})
    return serialize_doc(user)

async def insert_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)

async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return serialize_doc(user)

# -------------------------
# TRAVELS
# -------------------------
async def insert_travel(travel_data: dict):
    result = await travels_collection.insert_one(travel_data)
    return str(result.inserted_id)

async def get_travels_by_user(user_id: str, limit: int = 100):
    cursor = travels_collection.find({"user_id": user_id}).sort("date", -1).limit(limit)
    return [serialize_doc(doc) async for doc in cursor]

async def get_all_travels(limit: int = 1000):
    cursor = travels_collection.find().sort("date", -1).limit(limit)
    return [serialize_doc(doc) async for doc in cursor]
