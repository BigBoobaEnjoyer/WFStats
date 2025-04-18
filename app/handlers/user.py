from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependecy import get_user_service
from app.modules.user.exceptions import UsernameIsTakenException, WeakPasswordException
from app.modules.user import UserLoginSchema, UserCreateSchema
from app.modules.user import UserService

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
        await user_service.check_username_uniq(username=body.username)
    except UsernameIsTakenException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    try:
        user = await user_service.create_user(body.username, body.password)
    except WeakPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user
