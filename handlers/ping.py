from fastapi import FastAPI, APIRouter

router = APIRouter(prefix='/ping', tags=['ping'])


@router.get("/db")
async def ping_db():
    return {"text": "app is working"}

@router.get("/app")
async def ping_app():
    return {"text": "app is working"}