# src/demo/demo_vista.py
from models.reports.vista_oferta import VistaOferta
from config.database import SessionLocal

def demo_vista():
    """Demo de la vista VistaOferta"""
    db = SessionLocal()
    try:
        print("📊 Demo de VistaOferta")
        print("=" * 50)
        
        # Obtener algunos registros
        registros = db.query(VistaOferta).limit(5).all()
        
        for i, r in enumerate(registros, 1):
            print(f"{i}. {r.DNI}: {r.Nombre} {r.Apellido}")
            print(f"   Actividad: {r.Actividad} en {r.Sede}")
            print(f"   Estado: {r.estado_texto}")
            print()
            
    finally:
        db.close()

if __name__ == "__main__":
    demo_vista()