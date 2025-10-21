from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schemas para Conductor
class ConductorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    condicion_medica: Optional[str] = None
    horario_riesgo: Optional[str] = None
    activo: bool = True


class ConductorCreate(ConductorBase):
    pass


class ConductorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    condicion_medica: Optional[str] = None
    horario_riesgo: Optional[str] = None
    activo: Optional[bool] = None


class ConductorResponse(ConductorBase):
    id_conductor: int
    
    class Config:
        from_attributes = True


# Schemas para Viaje
class ViajeBase(BaseModel):
    id_conductor: int


class ViajeCreate(ViajeBase):
    pass


class ViajeFinalize(BaseModel):
    fecha_fin: datetime


class ViajeResponse(ViajeBase):
    id_viaje: int
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Schemas para LecturaSensor
class LecturaSensorBase(BaseModel):
    id_viaje: int
    percios: Optional[float] = None
    frecuencia_cardiaca: Optional[int] = None
    conteo_cabeceos: int = 0
    conteo_bostezos: int = 0


class LecturaSensorCreate(LecturaSensorBase):
    pass


class LecturaSensorResponse(LecturaSensorBase):
    id_lectura: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Schemas para Alerta
class AlertaBase(BaseModel):
    id_viaje: int
    tipo_alerta: str = Field(..., min_length=1, max_length=255)
    nivel_somnolencia: Optional[str] = None


class AlertaCreate(AlertaBase):
    pass


class AlertaResponse(AlertaBase):
    id_alerta: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Schemas adicionales para respuestas complejas
class ViajeDetalladoResponse(ViajeResponse):
    conductor: ConductorResponse
    lecturas: list[LecturaSensorResponse] = []
    alertas: list[AlertaResponse] = []
    
    class Config:
        from_attributes = True


class EstadisticasViajeResponse(BaseModel):
    id_viaje: int
    total_lecturas: int
    total_alertas: int
    frecuencia_cardiaca_promedio: Optional[float]
    total_cabeceos: int
    total_bostezos: int
    duracion_minutos: Optional[float]
