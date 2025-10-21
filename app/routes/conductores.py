from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.services.services import ConductorService
from app.schemas.schemas import ConductorCreate, ConductorUpdate, ConductorResponse

router = APIRouter(prefix="/conductores", tags=["Conductores"])


@router.get("/", response_model=List[ConductorResponse])
def listar_conductores(
    skip: int = 0,
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar todos los conductores registrados"""
    conductores = ConductorService.get_all(db, skip=skip, limit=limit, activo=activo)
    return conductores


@router.get("/{conductor_id}", response_model=ConductorResponse)
def obtener_conductor(conductor_id: int, db: Session = Depends(get_db)):
    """Obtener información de un conductor específico"""
    conductor = ConductorService.get_by_id(db, conductor_id)
    if not conductor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conductor con ID {conductor_id} no encontrado"
        )
    return conductor


@router.post("/", response_model=ConductorResponse, status_code=status.HTTP_201_CREATED)
def crear_conductor(conductor: ConductorCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo conductor en el sistema"""
    return ConductorService.create(db, conductor)


@router.put("/{conductor_id}", response_model=ConductorResponse)
def actualizar_conductor(
    conductor_id: int,
    conductor_update: ConductorUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar información de un conductor"""
    conductor = ConductorService.update(db, conductor_id, conductor_update)
    if not conductor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conductor con ID {conductor_id} no encontrado"
        )
    return conductor


@router.delete("/{conductor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_conductor(conductor_id: int, db: Session = Depends(get_db)):
    """Eliminar un conductor del sistema"""
    conductor = ConductorService.delete(db, conductor_id)
    if not conductor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conductor con ID {conductor_id} no encontrado"
        )
    return None
