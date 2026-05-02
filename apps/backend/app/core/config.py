from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_URL: str
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str

    class Config:
        env_file = ".env"


settings = Settings()