from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependecy import get_user_service
from app.exceptions.user import UsernameIsTakenException
from app.schema.user import UserLoginSchema, UserCreateSchema
from app.service.user import UserService

router = APIRouter(prefix='/user', tags=["user"])

@router.post('create', response_model=UserLoginSchema)
async def create_user(
        body:UserCreateSchema,
        user_service: Annotated[UserService,
        Depends(get_user_service)]
) -> UserLoginSchema:
    """
    Создание пользователя

    :param body: Логин, пароль
    :param user_service: Сервисный слой
    :return: Логин + JWT. UserLoginSchema
    """
    try:
        user_service.check_username_uniq(username=body.username)
    except UsernameIsTakenException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_service.create_user(body.username, body.password)
