from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PAGINATION_DEFAULT_LIMIT: int = 10
    PAGINATION_DEFAULT_LIMIT_MIN: int = 1
    PAGINATION_DEFAULT_LIMIT_MAX: int = 100

    class Config:
        env_file = '.env'


settings = Settings()
# 
