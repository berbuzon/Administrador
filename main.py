# main.py (ARCHIVO COMPLETO ACTUALIZADO)
import sys
import traceback
from datetime import datetime

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
        from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida
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
            print("\n📊 Obteniendo estadísticas de la vista...")
            stats = ReportService.get_estadisticas_vista(db)
            print(f"📈 Total de registros en la vista: {stats.get('total_registros', 0):,}")
            
            # Obtener datos por mes (usando método original)
            print("\n📅 Obteniendo adolescentes aceptados por mes desde 2025-03-17...")
            resultados = ReportService.get_adolescentes_aceptados_por_mes_vista(db)
            
            if not resultados:
                print("ℹ️ No se encontraron resultados con los filtros aplicados")
                print("Filtros: confirmado=1, asignada=1, estado=2, fecha>=2025-03-17")
                input("Presiona Enter para salir...")
                return
            
            # Mostrar resultados
            print("\n" + "=" * 50)
            print("📈 ADOLESCENTES ACEPTADOS POR MES")
            print("=" * 50)
            print(f"{'Año':<6} {'Mes':<6} {'Total':<10} {'Mes':<12}")
            print("-" * 40)
            
            total_general = 0
            for ano, mes, total in resultados:
                mes_nombre = datetime(2023, mes, 1).strftime('%B')
                print(f"{ano:<6} {mes:<6} {total:<10} {mes_nombre:<12}")
                total_general += total
            
            print("-" * 40)
            print(f"{'TOTAL GENERAL:':<20} {total_general:<10}")
            print(f"{'TOTAL MESES:':<20} {len(resultados):<10}")
            
            # DEMOSTRACIÓN DEL NUEVO OBJETO RECONSTRUIDO
            print("\n" + "=" * 60)
            print("🆕 DEMOSTRACIÓN VISTA OFERTA RECONSTRUIDA")
            print("=" * 60)
            
            # Obtener algunos registros reconstruidos
            print("🔍 Obteniendo primeros 3 registros reconstruidos...")
            registros_reconstruidos = ReportService.get_detalle_completo_vista_reconstruido(db, {
                'confirmado': True,
                'asignada': True,
                'estado': 2,
                'fecha_desde': '2025-03-17'
            })[:3]  # Solo primeros 3 para demo
            
            if registros_reconstruidos:
                print("✅ Registros reconstruidos obtenidos correctamente")
                print(f"📋 Mostrando {len(registros_reconstruidos)} registros de ejemplo:")
                print("-" * 80)
                
                for i, registro in enumerate(registros_reconstruidos, 1):
                    print(f"\n📄 REGISTRO {i}:")
                    print(f"   👤 Adolescente: {registro.nombre_completo}")
                    print(f"   🆔 DNI: {registro.dni_adolescente}")
                    print(f"   🏢 Sede: {registro.sede_nombre}")
                    print(f"   ⚽ Actividad: {registro.actividad_completa}")
                    print(f"   ✅ Estado: {registro.estado_texto}")
                    print(f"   📅 Actualizado: {registro.fecha_actualizacion}")
            
# main.py (ACTUALIZAR LA SECCIÓN DE EXPORTACIÓN)
# ... (código anterior permanece igual)

            # Exportar TODO en un solo archivo Excel con múltiples hojas
            print("\n💾 Generando archivo Excel único con múltiples hojas...")
            
            exportado = ReportService.exportar_todo_en_un_archivo(db, "reporte_adolescentes_aceptados.xlsx")
            
            if exportado:
                print("✅ Reporte completo exportado exitosamente")
                print("📊 Contenido del archivo:")
                print("   - Hoja 'Resumen Mensual': Resumen por meses")
                print("   - Hoja 'Detalle Completo': Detalle de todos los registros")
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
        print("📁 Archivo generado: reporte_adolescentes_aceptados.xlsx")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()