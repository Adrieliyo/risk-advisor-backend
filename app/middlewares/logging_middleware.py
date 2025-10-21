from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para registrar todas las peticiones HTTP"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log de la petición
        logger.info(f"Iniciando petición: {request.method} {request.url.path}")
        
        # Procesar la petición
        response = await call_next(request)
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Log de la respuesta
        logger.info(
            f"Petición completada: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Tiempo: {process_time:.3f}s"
        )
        
        # Añadir header con el tiempo de procesamiento
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
