from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Класс настроек"""
    DEBUG: str = ""
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = "log"
    REDIS_HOST: str = ""
    REDIS_PORT: int = 0
    REDIS_URL: str = "redis://redis-test:6379"
    PROJECT_NAME: str = "WEBSOCKET"

settings = Settings()

#print(Settings().model_dump())
print(settings.REDIS_HOST, settings.REDIS_PORT)