from app.models.models import LecturaSensor, Alerta
from app.schemas.schemas import AlertaCreate
from app.config.settings import settings
from sqlalchemy.orm import Session


class AlertaAutoDetector:
    """Servicio para detectar y generar alertas automáticamente basado en lecturas de sensores"""
    
    @staticmethod
    def analizar_lectura(db: Session, lectura: LecturaSensor) -> list[Alerta]:
        """
        Analiza una lectura de sensor y genera alertas si es necesario
        Retorna una lista de alertas generadas
        """
        alertas_generadas = []
        
        # Detectar frecuencia cardíaca anormal
        if lectura.frecuencia_cardiaca is not None:
            if lectura.frecuencia_cardiaca < settings.UMBRAL_FRECUENCIA_CARDIACA_MIN:
                alerta = AlertaCreate(
                    id_viaje=lectura.id_viaje,
                    tipo_alerta="FRECUENCIA_CARDIACA_BAJA",
                    nivel_somnolencia="MEDIO"
                )
                alertas_generadas.append(alerta)
            
            elif lectura.frecuencia_cardiaca > settings.UMBRAL_FRECUENCIA_CARDIACA_MAX:
                alerta = AlertaCreate(
                    id_viaje=lectura.id_viaje,
                    tipo_alerta="FRECUENCIA_CARDIACA_ALTA",
                    nivel_somnolencia="BAJO"
                )
                alertas_generadas.append(alerta)
        
        # Detectar cabeceos excesivos (señal de somnolencia)
        if lectura.conteo_cabeceos >= settings.UMBRAL_CABECEOS:
            nivel = "ALTO" if lectura.conteo_cabeceos >= settings.UMBRAL_CABECEOS * 2 else "MEDIO"
            alerta = AlertaCreate(
                id_viaje=lectura.id_viaje,
                tipo_alerta="SOMNOLENCIA_CABECEOS",
                nivel_somnolencia=nivel
            )
            alertas_generadas.append(alerta)
        
        # Detectar bostezos excesivos (señal de fatiga)
        if lectura.conteo_bostezos >= settings.UMBRAL_BOSTEZOS:
            nivel = "ALTO" if lectura.conteo_bostezos >= settings.UMBRAL_BOSTEZOS * 2 else "MEDIO"
            alerta = AlertaCreate(
                id_viaje=lectura.id_viaje,
                tipo_alerta="FATIGA_BOSTEZOS",
                nivel_somnolencia=nivel
            )
            alertas_generadas.append(alerta)
        
        # Detectar combinación peligrosa de cabeceos y bostezos
        if (lectura.conteo_cabeceos >= settings.UMBRAL_CABECEOS and 
            lectura.conteo_bostezos >= settings.UMBRAL_BOSTEZOS):
            alerta = AlertaCreate(
                id_viaje=lectura.id_viaje,
                tipo_alerta="PELIGRO_CRITICO",
                nivel_somnolencia="CRITICO"
            )
            alertas_generadas.append(alerta)
        
        # Guardar todas las alertas generadas en la base de datos
        db_alertas = []
        for alerta_create in alertas_generadas:
            db_alerta = Alerta(**alerta_create.model_dump())
            db.add(db_alerta)
            db_alertas.append(db_alerta)
        
        if db_alertas:
            db.commit()
            for alerta in db_alertas:
                db.refresh(alerta)
        
        return db_alertas
