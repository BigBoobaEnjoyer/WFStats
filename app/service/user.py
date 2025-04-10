import bcrypt

from dataclasses import dataclass

from app.repository import UserRepository
from app.schema.user import UserLoginSchema
from app.service.auth import AuthService
from app.exceptions.user import UsernameIsTakenException, WeakPasswordException


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


