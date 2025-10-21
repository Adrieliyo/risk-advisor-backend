from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "Risk Advisor API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Configuración de la base de datos
    DATABASE_URL: str
    
    # Configuración de seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    # Umbrales de alertas
    UMBRAL_FRECUENCIA_CARDIACA_MIN: int = 50
    UMBRAL_FRECUENCIA_CARDIACA_MAX: int = 120
    UMBRAL_CABECEOS: int = 3
    UMBRAL_BOSTEZOS: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
