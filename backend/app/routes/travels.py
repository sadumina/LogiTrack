from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_travels():
    return {"msg": "Travels route working"}
