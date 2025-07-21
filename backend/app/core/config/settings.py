from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str

    class Config:
        env_file = ".env"


settings = Settings()
