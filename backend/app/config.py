import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./ncd_chatbot.db"
    MONGODB_URI: str = ""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NCD Health Chatbot"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI/LLM settings
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    MODEL_NAME: str = "gpt-3.5-turbo"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]

    # SMTP Email Settings
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
