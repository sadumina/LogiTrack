from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, travels, admin

app = FastAPI(title="FuelTrackr API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ Later change to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(travels.router, prefix="/api/travels", tags=["Travels"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"msg": "✅ FuelTrackr API running"}
