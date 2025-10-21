"""
Script para poblar la base de datos con datos de ejemplo
Ejecutar con: python -m app.seeds.seed_data
"""
from app.config.database import SessionLocal
from app.models.models import Conductor, Viaje, LecturaSensor, Alerta
from datetime import datetime, timedelta
import random


def seed_database():
    """Poblar la base de datos con datos de ejemplo"""
    db = SessionLocal()
    
    try:
        print("Iniciando seed de la base de datos...")
        
        # Limpiar datos existentes (opcional)
        print("\n1. Limpiando datos existentes...")
        db.query(Alerta).delete()
        db.query(LecturaSensor).delete()
        db.query(Viaje).delete()
        db.query(Conductor).delete()
        db.commit()
        
        # Crear conductores
        print("\n2. Creando conductores...")
        conductores = [
            Conductor(
                nombre="Juan Pérez",
                condicion_medica="Ninguna",
                horario_riesgo="22:00-06:00",
                activo=True
            ),
            Conductor(
                nombre="María García",
                condicion_medica="Hipertensión",
                horario_riesgo="00:00-08:00",
                activo=True
            ),
            Conductor(
                nombre="Carlos Rodríguez",
                condicion_medica="Diabetes",
                horario_riesgo="23:00-07:00",
                activo=True
            ),
            Conductor(
                nombre="Ana Martínez",
                condicion_medica="Ninguna",
                horario_riesgo="01:00-09:00",
                activo=False
            ),
        ]
        
        for conductor in conductores:
            db.add(conductor)
        db.commit()
        print(f"   ✓ {len(conductores)} conductores creados")
        
        # Crear viajes
        print("\n3. Creando viajes...")
        viajes = []
        for i, conductor in enumerate(conductores[:3]):  # Solo los activos
            # Viaje finalizado
            fecha_inicio = datetime.now() - timedelta(days=i+1, hours=2)
            viaje1 = Viaje(
                id_conductor=conductor.id_conductor,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_inicio + timedelta(hours=random.randint(1, 4))
            )
            db.add(viaje1)
            viajes.append(viaje1)
            
            # Viaje activo (sin fecha_fin)
            if i == 0:  # Solo el primer conductor tiene viaje activo
                viaje2 = Viaje(
                    id_conductor=conductor.id_conductor,
                    fecha_inicio=datetime.now() - timedelta(minutes=30),
                    fecha_fin=None
                )
                db.add(viaje2)
                viajes.append(viaje2)
        
        db.commit()
        print(f"   ✓ {len(viajes)} viajes creados")
        
        # Crear lecturas de sensores
        print("\n4. Creando lecturas de sensores...")
        lecturas_count = 0
        for viaje in viajes:
            num_lecturas = random.randint(5, 15)
            for j in range(num_lecturas):
                timestamp = viaje.fecha_inicio + timedelta(minutes=j*5)
                lectura = LecturaSensor(
                    id_viaje=viaje.id_viaje,
                    timestamp=timestamp,
                    percios=round(random.uniform(0.5, 2.0), 2),
                    frecuencia_cardiaca=random.randint(55, 115),
                    conteo_cabeceos=random.randint(0, 6),
                    conteo_bostezos=random.randint(0, 8)
                )
                db.add(lectura)
                lecturas_count += 1
        
        db.commit()
        print(f"   ✓ {lecturas_count} lecturas de sensores creadas")
        
        # Crear alertas
        print("\n5. Creando alertas...")
        alertas = [
            Alerta(
                id_viaje=viajes[0].id_viaje,
                timestamp=viajes[0].fecha_inicio + timedelta(minutes=20),
                tipo_alerta="SOMNOLENCIA_CABECEOS",
                nivel_somnolencia="MEDIO"
            ),
            Alerta(
                id_viaje=viajes[0].id_viaje,
                timestamp=viajes[0].fecha_inicio + timedelta(minutes=45),
                tipo_alerta="FATIGA_BOSTEZOS",
                nivel_somnolencia="ALTO"
            ),
            Alerta(
                id_viaje=viajes[1].id_viaje,
                timestamp=viajes[1].fecha_inicio + timedelta(minutes=30),
                tipo_alerta="FRECUENCIA_CARDIACA_ALTA",
                nivel_somnolencia="BAJO"
            ),
        ]
        
        for alerta in alertas:
            db.add(alerta)
        db.commit()
        print(f"   ✓ {len(alertas)} alertas creadas")
        
        print("\n✅ Seed completado exitosamente!")
        print("\nResumen:")
        print(f"  - Conductores: {len(conductores)}")
        print(f"  - Viajes: {len(viajes)}")
        print(f"  - Lecturas: {lecturas_count}")
        print(f"  - Alertas: {len(alertas)}")
        
    except Exception as e:
        print(f"\n❌ Error durante el seed: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
