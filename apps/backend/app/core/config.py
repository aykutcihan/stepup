from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str = ""
    FRONTEND_URL: str
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    class Config:
        env_file = ".env"


settings = Settings()