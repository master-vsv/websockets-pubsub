from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Класс настроек"""
    DEBUG: str = ""
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = "log"
    REDIS_HOST: str = ""
    REDIS_PORT: int = ""
    REDIS_URL: str = ""

settings = Settings()

#print(Settings().model_dump())
print(settings.REDIS_HOST, settings.REDIS_PORT)