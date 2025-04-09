from fastapi import Depends, security, HTTPException
from fastapi.params import Security
from sqlalchemy.orm import Session

from app.infrastracture.cache.repository import PlayerCacheRepository
from app.infrastracture.database.database import get_db_session, get_async_db_session
from app.exceptions.auth import TokenExpired, TokenIncorrect
from app.repository.player import PlayerRepository
from app.repository.user import UserRepository
from app.service.auth import AuthService
from app.service.players import WFApiPlayer
from app.service.user import UserService
from app.settings import Settings
from app.infrastracture.cache.accessor import get_cache_session


def get_players_repository() -> PlayerRepository:
    db_session = get_db_session()
    return PlayerRepository(db_session)

def get_players_repository_async() -> PlayerRepository:
    db_session = get_async_db_session()
    return PlayerRepository(db_session)

def get_player_cache_repository() -> PlayerCacheRepository:
    cache_session = get_cache_session()
    player_repository = get_players_repository_async()
    return PlayerCacheRepository(
        cache_session=cache_session,
        player_repository=player_repository
    )

def get_wf_api_players_service(
        player_repository = Depends(get_players_repository_async)
) -> WFApiPlayer:
    return WFApiPlayer(player_repository=player_repository)

def get_wf_api_players_service_redis(
        player_repository = Depends(get_players_repository_async),
        player_cache_repository = Depends(get_player_cache_repository)
) -> WFApiPlayer:
    return WFApiPlayer(player_repository= player_repository, player_cache_repository=player_cache_repository)

def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)

def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())

def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
) ->UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)

reusable_oauth2 = security.HTTPBearer()

def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail= e.detail
        )
    except TokenIncorrect as e:
        raise HTTPException(
            status_code=401,
            detail= e.detail
        )
    return user_id
