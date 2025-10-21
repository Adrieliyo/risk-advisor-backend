from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.config.database import get_db
from app.services.services import ViajeService
from app.schemas.schemas import (
    ViajeCreate,
    ViajeResponse,
    ViajeDetalladoResponse,
    EstadisticasViajeResponse,
    ViajeFinalize,
)

router = APIRouter(prefix="/viajes", tags=["Viajes"])


@router.get("/", response_model=List[ViajeResponse])
def listar_viajes(
    skip: int = 0,
    limit: int = 100,
    conductor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar todos los viajes registrados"""
    viajes = ViajeService.get_all(db, skip=skip, limit=limit, conductor_id=conductor_id)
    return viajes


@router.get("/{viaje_id}", response_model=ViajeDetalladoResponse)
def obtener_viaje(viaje_id: int, db: Session = Depends(get_db)):
    """Obtener información detallada de un viaje específico"""
    viaje = ViajeService.get_by_id(db, viaje_id)
    if not viaje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Viaje con ID {viaje_id} no encontrado"
        )
    return viaje


@router.get("/{viaje_id}/estadisticas", response_model=EstadisticasViajeResponse)
def obtener_estadisticas_viaje(viaje_id: int, db: Session = Depends(get_db)):
    """Obtener estadísticas de un viaje"""
    estadisticas = ViajeService.get_estadisticas(db, viaje_id)
    if not estadisticas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Viaje con ID {viaje_id} no encontrado"
        )
    return estadisticas


@router.get("/conductor/{conductor_id}/activo", response_model=Optional[ViajeResponse])
def obtener_viaje_activo(conductor_id: int, db: Session = Depends(get_db)):
    """Obtener el viaje activo de un conductor"""
    viaje = ViajeService.get_active_by_conductor(db, conductor_id)
    return viaje


@router.post("/", response_model=ViajeResponse, status_code=status.HTTP_201_CREATED)
def iniciar_viaje(viaje: ViajeCreate, db: Session = Depends(get_db)):
    """Iniciar un nuevo viaje"""
    try:
        return ViajeService.create(db, viaje)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{viaje_id}/finalizar", response_model=ViajeResponse)
def finalizar_viaje(
    viaje_id: int,
    viaje_fin: ViajeFinalize,
    db: Session = Depends(get_db)
):
    """Finalizar un viaje en curso"""
    viaje = ViajeService.finalize(db, viaje_id, viaje_fin.fecha_fin)
    if not viaje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Viaje con ID {viaje_id} no encontrado"
        )
    return viaje
