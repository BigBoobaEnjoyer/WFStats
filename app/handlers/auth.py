from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.dependecy import get_auth_service
from app.exceptions.auth import  IncorrectAuthPasswordException
from app.exceptions.user import UserNotFoundException
from app.schema import UserCreateSchema, UserLoginSchema
from app.service.auth import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login')
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserLoginSchema:
    """
    Авторизация

    :param body: Логин, пароль
    :param auth_service: сервисный слой
    :return: Логин, JWT. UserLoginSchema
    """
    try:
        await auth_service.login(body.username, body.password)
    except UserNotFoundException as ex:
        raise HTTPException(
            status_code=404
        )
    except IncorrectAuthPasswordException as ex:
        raise HTTPException(
            status_code=401
        )
    return await auth_service.login(body.username, body.password)
