from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.config.settings import settings
from app.config.database import engine, Base
from app.middlewares.error_handler import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler,
)
from app.middlewares.logging_middleware import LoggingMiddleware

# Importar rutas
from app.routes import conductores, viajes, lecturas, alertas

# Nota: Las tablas se crean con el script: python -m app.utils.create_tables
# Base.metadata.create_all(bind=engine)

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Risk Advisor API
    
    Sistema de monitoreo y gestión de conductores que registra lecturas de sensores 
    y genera alertas basadas en condiciones de riesgo.
    
    ### Características principales:
    
    * **Gestión de Conductores**: Registro y administración de conductores
    * **Monitoreo de Viajes**: Seguimiento de viajes en tiempo real
    * **Lecturas de Sensores**: Captura de datos de sensores (frecuencia cardíaca, bostezos, cabeceos)
    * **Sistema de Alertas**: Generación automática de alertas basadas en umbrales de riesgo
    * **Análisis de Datos**: Estadísticas y análisis de viajes
    
    ### Detección automática de riesgos:
    
    El sistema analiza automáticamente cada lectura de sensores y genera alertas cuando detecta:
    - Somnolencia (cabeceos frecuentes)
    - Fatiga (bostezos excesivos)
    - Anomalías en frecuencia cardíaca
    - Situaciones de peligro crítico
    """,
    debug=settings.DEBUG,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de logging
app.add_middleware(LoggingMiddleware)

# Registrar manejadores de excepciones
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Incluir routers
app.include_router(conductores.router)
app.include_router(viajes.router)
app.include_router(lecturas.router)
app.include_router(alertas.router)


@app.get("/", tags=["Root"])
def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Bienvenido a Risk Advisor API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
