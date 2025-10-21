from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.services.services import LecturaSensorService
from app.services.alerta_detector import AlertaAutoDetector
from app.schemas.schemas import LecturaSensorCreate, LecturaSensorResponse

router = APIRouter(prefix="/lecturas", tags=["Lecturas de Sensores"])


@router.get("/viaje/{viaje_id}", response_model=List[LecturaSensorResponse])
def listar_lecturas_viaje(
    viaje_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar todas las lecturas de sensores de un viaje"""
    lecturas = LecturaSensorService.get_all(db, viaje_id, skip=skip, limit=limit)
    return lecturas


@router.get("/{lectura_id}", response_model=LecturaSensorResponse)
def obtener_lectura(lectura_id: int, db: Session = Depends(get_db)):
    """Obtener información de una lectura específica"""
    lectura = LecturaSensorService.get_by_id(db, lectura_id)
    if not lectura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura con ID {lectura_id} no encontrada"
        )
    return lectura


@router.post("/", response_model=LecturaSensorResponse, status_code=status.HTTP_201_CREATED)
def crear_lectura(lectura: LecturaSensorCreate, db: Session = Depends(get_db)):
    """
    Registrar una nueva lectura de sensores
    El sistema automáticamente analizará la lectura y generará alertas si es necesario
    """
    # Crear la lectura
    db_lectura = LecturaSensorService.create(db, lectura)
    
    # Analizar automáticamente y generar alertas si es necesario
    AlertaAutoDetector.analizar_lectura(db, db_lectura)
    
    return db_lectura
