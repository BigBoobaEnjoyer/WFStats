from pydantic_settings import  BaseSettings

class Settings(BaseSettings):
    JWT_SECRET:str = 'secret'
    JWT_ALGORITHM:str = 'HS256'
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
