from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, travels, admin
from app.database import db

app = FastAPI(title="FuelTrackr API")

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this later to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include Routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(travels.router, prefix="/api/travels", tags=["Travels"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# ✅ Startup event — check DB connection
@app.on_event("startup")
async def startup_db_client():
    try:
        await db.command("ping")
        print("✅ MongoDB connection established successfully")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

# ✅ Root endpoint
@app.get("/")
async def root():
    return {"msg": "🚀 FuelTrackr API running"}
