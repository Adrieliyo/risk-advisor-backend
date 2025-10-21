"""
Script para crear las tablas de la base de datos
Ejecutar con: python -m app.utils.create_tables
"""
from app.config.database import engine, Base
from app.models.models import Conductor, Viaje, LecturaSensor, Alerta

def create_tables():
    """Crear todas las tablas en la base de datos"""
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente!")
    print("\nTablas creadas:")
    print("  - conductores")
    print("  - viajes")
    print("  - lecturas_sensores")
    print("  - alertas")

if __name__ == "__main__":
    create_tables()
