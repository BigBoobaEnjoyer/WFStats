from fastapi import FastAPI, APIRouter

router = APIRouter(prefix='/ping', tags=['ping'])

@router.get("/app")
async def ping_app():
    """
    довольно бесполезная проверка "ничего"

    :return: dict с сообщением
    """
    return {"text": "app is working"}