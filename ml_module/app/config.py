from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Databas
    DB_HOST: str = "postgres"  # Container-namn i Docker Network
    DB_PORT: int = 5432
    DB_NAME: str = "book_db"
    DB_USER: str = "book_user"
    DB_PASSWORD: str = "book_password"

    # Cache (Redis)
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    CACHE_TTL_SECONDS: int = 3600  # 1 timme

    # Modellinställningar
    TOP_N_RECOMMENDATIONS: int = 10
    MODEL_SAVE_PATH: str = "/app/models/saved_models"

    class Config:
        env_file = ".env"

settings = Settings()
