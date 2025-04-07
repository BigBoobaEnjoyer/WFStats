from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from dependecy import get_auth_service
from exceptions.auth import  IncorrectAuthPasswordException
from exceptions.user import UserNotFoundException
from schema import UserCreateSchema
from service.auth import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login')
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):

    try:
        auth_service.login(body.username, body.password)

    except UserNotFoundException as ex:
        raise HTTPException(
            status_code=404
        )

    except IncorrectAuthPasswordException as ex:
        raise HTTPException(
            status_code=401
        )

    return auth_service.login(body.username, body.password)