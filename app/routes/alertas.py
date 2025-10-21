from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.services.services import AlertaService
from app.schemas.schemas import AlertaCreate, AlertaResponse

router = APIRouter(prefix="/alertas", tags=["Alertas"])


@router.get("/", response_model=List[AlertaResponse])
def listar_alertas(
    skip: int = 0,
    limit: int = 100,
    viaje_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar todas las alertas del sistema"""
    alertas = AlertaService.get_all(db, viaje_id=viaje_id, skip=skip, limit=limit)
    return alertas


@router.get("/recientes", response_model=List[AlertaResponse])
def listar_alertas_recientes(limit: int = 10, db: Session = Depends(get_db)):
    """Obtener las alertas más recientes del sistema"""
    alertas = AlertaService.get_alertas_recientes(db, limit=limit)
    return alertas


@router.get("/{alerta_id}", response_model=AlertaResponse)
def obtener_alerta(alerta_id: int, db: Session = Depends(get_db)):
    """Obtener información de una alerta específica"""
    alerta = AlertaService.get_by_id(db, alerta_id)
    if not alerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alerta con ID {alerta_id} no encontrada"
        )
    return alerta


@router.post("/", response_model=AlertaResponse, status_code=status.HTTP_201_CREATED)
def crear_alerta_manual(alerta: AlertaCreate, db: Session = Depends(get_db)):
    """Crear una alerta manualmente (normalmente se generan automáticamente)"""
    return AlertaService.create(db, alerta)
