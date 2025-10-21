from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base


class Conductor(Base):
    __tablename__ = "conductores"
    
    id_conductor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    condicion_medica = Column(String, nullable=True)
    horario_riesgo = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    viajes = relationship("Viaje", back_populates="conductor")


class Viaje(Base):
    __tablename__ = "viajes"
    
    id_viaje = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_conductor = Column(Integer, ForeignKey("conductores.id_conductor"), nullable=False)
    fecha_inicio = Column(DateTime(timezone=True), default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
    
    # Relaciones
    conductor = relationship("Conductor", back_populates="viajes")
    lecturas = relationship("LecturaSensor", back_populates="viaje")
    alertas = relationship("Alerta", back_populates="viaje")


class LecturaSensor(Base):
    __tablename__ = "lecturas_sensores"
    
    id_lectura = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_viaje = Column(Integer, ForeignKey("viajes.id_viaje"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    percios = Column(Float, nullable=True)
    frecuencia_cardiaca = Column(Integer, nullable=True)
    conteo_cabeceos = Column(Integer, default=0)
    conteo_bostezos = Column(Integer, default=0)
    
    # Relaciones
    viaje = relationship("Viaje", back_populates="lecturas")


class Alerta(Base):
    __tablename__ = "alertas"
    
    id_alerta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_viaje = Column(Integer, ForeignKey("viajes.id_viaje"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tipo_alerta = Column(String, nullable=False)
    nivel_somnolencia = Column(String, nullable=True)
    
    # Relaciones
    viaje = relationship("Viaje", back_populates="alertas")
