from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Conductor, Viaje, LecturaSensor, Alerta
from app.schemas.schemas import (
    ConductorCreate,
    ConductorUpdate,
    ViajeCreate,
    LecturaSensorCreate,
    AlertaCreate,
)
from datetime import datetime
from typing import Optional


class ConductorService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None):
        query = db.query(Conductor)
        if activo is not None:
            query = query.filter(Conductor.activo == activo)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, conductor_id: int):
        return db.query(Conductor).filter(Conductor.id_conductor == conductor_id).first()
    
    @staticmethod
    def create(db: Session, conductor: ConductorCreate):
        db_conductor = Conductor(**conductor.model_dump())
        db.add(db_conductor)
        db.commit()
        db.refresh(db_conductor)
        return db_conductor
    
    @staticmethod
    def update(db: Session, conductor_id: int, conductor_update: ConductorUpdate):
        db_conductor = db.query(Conductor).filter(Conductor.id_conductor == conductor_id).first()
        if db_conductor:
            update_data = conductor_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_conductor, key, value)
            db.commit()
            db.refresh(db_conductor)
        return db_conductor
    
    @staticmethod
    def delete(db: Session, conductor_id: int):
        db_conductor = db.query(Conductor).filter(Conductor.id_conductor == conductor_id).first()
        if db_conductor:
            db.delete(db_conductor)
            db.commit()
        return db_conductor


class ViajeService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, conductor_id: Optional[int] = None):
        query = db.query(Viaje)
        if conductor_id:
            query = query.filter(Viaje.id_conductor == conductor_id)
        return query.order_by(Viaje.fecha_inicio.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, viaje_id: int):
        return db.query(Viaje).filter(Viaje.id_viaje == viaje_id).first()
    
    @staticmethod
    def get_active_by_conductor(db: Session, conductor_id: int):
        """Obtiene el viaje activo (sin fecha_fin) de un conductor"""
        return db.query(Viaje).filter(
            Viaje.id_conductor == conductor_id,
            Viaje.fecha_fin == None
        ).first()
    
    @staticmethod
    def create(db: Session, viaje: ViajeCreate):
        # Verificar que no hay un viaje activo para este conductor
        viaje_activo = ViajeService.get_active_by_conductor(db, viaje.id_conductor)
        if viaje_activo:
            raise ValueError("El conductor ya tiene un viaje activo")
        
        db_viaje = Viaje(**viaje.model_dump())
        db.add(db_viaje)
        db.commit()
        db.refresh(db_viaje)
        return db_viaje
    
    @staticmethod
    def finalize(db: Session, viaje_id: int, fecha_fin: datetime):
        db_viaje = db.query(Viaje).filter(Viaje.id_viaje == viaje_id).first()
        if db_viaje:
            db_viaje.fecha_fin = fecha_fin
            db.commit()
            db.refresh(db_viaje)
        return db_viaje
    
    @staticmethod
    def get_estadisticas(db: Session, viaje_id: int):
        viaje = db.query(Viaje).filter(Viaje.id_viaje == viaje_id).first()
        if not viaje:
            return None
        
        # Obtener estadísticas de lecturas
        lecturas_stats = db.query(
            func.count(LecturaSensor.id_lectura).label("total_lecturas"),
            func.avg(LecturaSensor.frecuencia_cardiaca).label("fc_promedio"),
            func.sum(LecturaSensor.conteo_cabeceos).label("total_cabeceos"),
            func.sum(LecturaSensor.conteo_bostezos).label("total_bostezos")
        ).filter(LecturaSensor.id_viaje == viaje_id).first()
        
        # Contar alertas
        total_alertas = db.query(func.count(Alerta.id_alerta)).filter(
            Alerta.id_viaje == viaje_id
        ).scalar()
        
        # Calcular duración
        duracion_minutos = None
        if viaje.fecha_fin:
            duracion = viaje.fecha_fin - viaje.fecha_inicio
            duracion_minutos = duracion.total_seconds() / 60
        
        return {
            "id_viaje": viaje_id,
            "total_lecturas": lecturas_stats.total_lecturas or 0,
            "total_alertas": total_alertas or 0,
            "frecuencia_cardiaca_promedio": float(lecturas_stats.fc_promedio) if lecturas_stats.fc_promedio else None,
            "total_cabeceos": lecturas_stats.total_cabeceos or 0,
            "total_bostezos": lecturas_stats.total_bostezos or 0,
            "duracion_minutos": duracion_minutos
        }


class LecturaSensorService:
    @staticmethod
    def get_all(db: Session, viaje_id: int, skip: int = 0, limit: int = 100):
        return db.query(LecturaSensor).filter(
            LecturaSensor.id_viaje == viaje_id
        ).order_by(LecturaSensor.timestamp.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, lectura_id: int):
        return db.query(LecturaSensor).filter(LecturaSensor.id_lectura == lectura_id).first()
    
    @staticmethod
    def create(db: Session, lectura: LecturaSensorCreate):
        db_lectura = LecturaSensor(**lectura.model_dump())
        db.add(db_lectura)
        db.commit()
        db.refresh(db_lectura)
        return db_lectura


class AlertaService:
    @staticmethod
    def get_all(db: Session, viaje_id: Optional[int] = None, skip: int = 0, limit: int = 100):
        query = db.query(Alerta)
        if viaje_id:
            query = query.filter(Alerta.id_viaje == viaje_id)
        return query.order_by(Alerta.timestamp.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, alerta_id: int):
        return db.query(Alerta).filter(Alerta.id_alerta == alerta_id).first()
    
    @staticmethod
    def create(db: Session, alerta: AlertaCreate):
        db_alerta = Alerta(**alerta.model_dump())
        db.add(db_alerta)
        db.commit()
        db.refresh(db_alerta)
        return db_alerta
    
    @staticmethod
    def get_alertas_recientes(db: Session, limit: int = 10):
        """Obtiene las alertas más recientes del sistema"""
        return db.query(Alerta).order_by(Alerta.timestamp.desc()).limit(limit).all()
