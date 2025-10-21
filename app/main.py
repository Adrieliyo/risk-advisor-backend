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

from app.routes import conductores, viajes, lecturas, alertas

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
   el padilla se come los mocos
    """,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

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
