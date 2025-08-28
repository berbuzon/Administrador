from config.database import SessionLocal, test_connection
from services.report_service import ReportService
import pandas as pd
from datetime import datetime

import sys
import os
print("🐍 Python version:", sys.version)
print("📁 Working directory:", os.getcwd())
print("🚀 Starting main.py...")
sys.stdout.flush()

def main():
    print("Iniciando aplicación con vista vista_oferta...")
    print("=" * 60)
    
    # Verificar conexión
    if not test_connection():
        return
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # Obtener estadísticas generales de la vista
        print("\n📊 Obteniendo estadísticas de la vista...")
        stats = ReportService.get_estadisticas_vista(db)
        
        print(f"📈 Total de registros en vista: {stats.get('total_registros', 0)}")
        
        # Obtener datos por mes desde la vista
        print("\n📅 Obteniendo adolescentes aceptados por mes desde 2025-03-17...")
        resultados = ReportService.get_adolescentes_aceptados_por_mes_vista(db)
        
        if not resultados:
            print("ℹ️ No se encontraron resultados con los filtros aplicados")
            return
        
        # Mostrar resultados
        print("\n" + "=" * 50)
        print("📈 ADOLESCENTES ACEPTADOS POR MES (VISTA)")
        print("=" * 50)
        print(f"{'Año':<6} {'Mes':<6} {'Total':<8} {'Mes':<12}")
        print("-" * 40)
        
        total_general = 0
        for ano, mes, total in resultados:
            mes_nombre = datetime(2023, mes, 1).strftime('%B')
            print(f"{ano:<6} {mes:<6} {total:<8} {mes_nombre:<12}")
            total_general += total
        
        print("-" * 40)
        print(f"{'TOTAL GENERAL:':<20} {total_general:<8}")
        
        # Exportar detalle completo
        print("\n💾 Exportando detalle completo...")
        success = ReportService.exportar_detalle_completo(db)
        
        if success:
            print("✓ Exportación completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
        print("\n🔌 Conexión a base de datos cerrada.")

if __name__ == "__main__":
    main()