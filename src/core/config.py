from pydantic_settings import BaseSettings
from functools import lru_cache
from src.core.enums import TranslationEngine


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    APP_NAME: str = "Translation Service API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Translation Engine Configuration
    TRANSLATION_ENGINE: TranslationEngine = TranslationEngine.LOCAL
    
    # Google Translate Configuration
    GOOGLE_PROJECT_ID: str = ""
    GOOGLE_CREDENTIALS_PATH: str = ""  # Path to service account JSON
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Local GPU Configuration
    LOCAL_MODEL_NAME: str = "facebook/nllb-200-distilled-600M"
    LOCAL_DEVICE: str = "cuda"  # "cuda" or "cpu"
    LOCAL_MODEL_PRECISION: str = "float32"  # "float32" or "float16"
    LOCAL_BATCH_SIZE: int = 8
    LOCAL_MAX_LENGTH: int = 512
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/translation_db"
    DB_ECHO: bool = False
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # API Configuration
    MAX_TEXT_LENGTH: int = 5000
    MAX_BATCH_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()
