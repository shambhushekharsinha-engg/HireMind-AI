import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "HireMind AI – AI-Powered Career Intelligence Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "hiremind_ai_super_secret_jwt_key_2026_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database: SQLite for fast local dev, ready for PostgreSQL in production
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hiremind.db")
    
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "generated_reports")

    class Config:
        case_sensitive = True

settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORTS_DIR, exist_ok=True)