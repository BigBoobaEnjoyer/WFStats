from pydantic_settings import  BaseSettings

class Settings(BaseSettings):
    JWT_SECRET:str = 'secret'
    JWT_ALGORITHM:str = 'HS256'