import bcrypt
from jose import jwt, JWTError

from dataclasses import dataclass

from datetime import datetime, UTC, timedelta
from app.infrastracture.database.models import UserProfile
from app.modules.user import UserRepository
from app.modules.user import UserLoginSchema
from app.modules.user import UserNotFoundException, IncorrectAuthPasswordException, \
    TokenIncorrect, TokenExpired


from app.modules.user import UsernameIsTakenException
from app.settings import Settings


@dataclass
class AuthService:

    user_repository: UserRepository
    settings: Settings

    async def login(self, username:str, password:str) -> UserLoginSchema:
        user: UserProfile = await self.user_repository.get_user_by_username(username)
        access_token = await self.generate_access_token(user_id=user.id)
        if not user:
            raise UserNotFoundException(UserNotFoundException.detail)
        elif not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise IncorrectAuthPasswordException
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    async def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (datetime.now(UTC) + timedelta(weeks=1)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'expire': expires_date_unix},
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM
        )
        return token

    async def get_user_id_from_access_token(self, access_token: str ) -> int:
        try:
            payload = jwt.decode(
            token=access_token,
            algorithms=self.settings.JWT_ALGORITHM,
            key=self.settings.JWT_SECRET,
            )
        except JWTError:
            raise TokenIncorrect
        if payload['expire'] < datetime.now(UTC).timestamp():
            raise TokenExpired
        return payload['user_id']

@dataclass
class UserService:
    user_repository: UserRepository
    auth_service : AuthService

    async def create_user(self, username:str, password: str) -> UserLoginSchema:
        hashed: str = await self.password_hash(password)
        user = await self.user_repository.create_user(username=username, password=hashed)
        token = await self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=token)

    async def check_username_uniq(self, username: str):
        if await self.user_repository.get_user_by_username(username):
            raise UsernameIsTakenException(UsernameIsTakenException.detail)

    @staticmethod
    async def password_hash( password: str) -> str:
        salt:bytes = bcrypt.gensalt()
        pass_hash:bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
        return pass_hash.decode('utf-8')

