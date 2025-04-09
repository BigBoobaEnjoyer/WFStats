from dataclasses import dataclass


from app.repository import UserRepository
from app.schema.user import UserLoginSchema
from app.service.auth import AuthService
from app.exceptions.user import UsernameIsTakenException


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service : AuthService

    def create_user(self, username:str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(username=username, password=password)
        token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=token)

    def check_username_uniq(self, username: str):
        if self.user_repository.get_user_by_username(username):
            raise UsernameIsTakenException(UsernameIsTakenException.detail)