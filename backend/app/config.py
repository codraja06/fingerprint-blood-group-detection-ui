from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BloodID API"
    MONGODB_URL: str = "mongodb://localhost:27017/bloodid"
    JWT_SECRET: str = "change_this_to_a_secure_random_string_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    class Config:
        env_file = ".env"

settings = Settings()
