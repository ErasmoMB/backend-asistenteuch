from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    # Configuración de voz
    VOICE_LANGUAGE: str = "spanish"
    VOICE_RATE: int = 150
    
    # Configuración de la aplicación
    APP_NAME: str = "Asistente Virtual"
    DEBUG: bool = True
    
    # API Keys
    GEMINI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 