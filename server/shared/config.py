from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Hominun RPG Server"
    debug: bool = False
    database_url: str
    redis_url: str = "redis://localhost:6379"
    secret_key: str
    save_version: int = 1
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    class Config:
        env_file = ".env"


settings = Settings()
