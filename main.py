# main.py
import sys
import traceback

# Configurar el output para que se muestre inmediatamente
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

def main():
    try:
        print("🚀 Iniciando aplicación de reportes...")
        print("=" * 60)
        
        # Importar módulos
        print("📦 Importando módulos...")
        from config.database import SessionLocal, test_connection
        from services.report_service import ReportService
        import pandas as pd
        
        print("✅ Módulos importados correctamente")
        
        # Verificar conexión a la base de datos
        print("\n🔌 Probando conexión a la base de datos...")
        if not test_connection():
            print("❌ La conexión a la base de datos falló")
            input("Presiona Enter para salir...")
            return
        
        print("✅ Conexión a la base de datos exitosa")
        
        # Crear sesión de base de datos
        db = SessionLocal()
        
        try:
            # Exportar TODO sin filtros
            print("\n💾 Exportando TODOS los datos a Excel...")
            exportado = ReportService.exportar_todo_a_excel(db, "reporte_completo.xlsx")
            
            if exportado:
                print("✅ Reporte completo exportado exitosamente")
                print("📊 Contenido del archivo:")
                print("   - Hoja 'Vista_oferta': Todos los datos crudos")
                print("   - Hoja 'Vista_oferta_reconstruida': Todos los datos reconstruidos")
            else:
                print("⚠️ No se pudo exportar el reporte completo")
        
        except Exception as e:
            print(f"❌ Error durante el procesamiento: {str(e)}")
            traceback.print_exc()
        
        finally:
            db.close()
            print("\n🔌 Conexión a base de datos cerrada")
    
    except ImportError as e:
        print(f"❌ Error de importación: {str(e)}")
        print("💡 Verifica que todos los módulos estén instalados correctamente")
        traceback.print_exc()
    
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        traceback.print_exc()
    
    finally:
        print("\n🏁 Ejecución completada")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()