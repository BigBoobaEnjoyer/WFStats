from dataclasses import dataclass
import datetime

from jose import jwt, JWTError

from exceptions.auth import IncorrectAuthPasswordException, TokenExpired, TokenIncorrect
from exceptions.user import UserNotFoundException
from database.models import UserProfile
from schema.user import UserLoginSchema
from repository.user import UserRepository
from settings import Settings

@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    def login(self, username:str, password:str) -> UserLoginSchema:
        user: UserProfile = self.user_repository.get_user_by_username(username)
        access_token = self.generate_access_token(user_id=user.id)
        if not user:
            raise UserNotFoundException(UserNotFoundException.detail)
        elif user.password != password:
            raise IncorrectAuthPasswordException
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(weeks=1)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'expire': expires_date_unix},
            self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str ) -> int:
        try:
            payload = jwt.decode(
            token=access_token,
            algorithms=self.settings.JWT_ALGORITHM,
            key=self.settings.JWT_SECRET,
            )
        except JWTError:
            raise TokenIncorrect
        if payload['expire'] < datetime.datetime.now(datetime.UTC).timestamp():
            raise TokenExpired
        return payload['user_id']
