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
                print("   - Hojas 'Confirmados_[mes]': Adolescentes confirmados por mes")
            else:
                print("⚠️ No se pudo exportar el reporte completo")
            
            # Análisis de secuencias (DENTRO del mismo try, antes de cerrar la conexión)
            print("\n🔍 Analizando secuencias de estados y asignaciones...")
            
            # Obtener datos reconstruidos para el análisis
            datos_para_analisis = ReportService.get_vista_oferta_reconstruida(db)
            
            analisis_exportado = ReportService.analizar_secuencias(
                datos_para_analisis, 
                "analisis_secuencias.xlsx"
            )
            
            if analisis_exportado:
                print("✅ Análisis de secuencias completado exitosamente")
                print("📊 Contenido del archivo:")
                print("   - Hoja 'detalle_secuencia': Detalle de cada paso por formulario")
                print("   - Hoja 'resumen_por_formulario': Secuencia completa por formulario")
                print("   - Hoja 'frecuencia_secuencias': Frecuencia de cada secuencia")
            else:
                print("⚠️ No se pudo completar el análisis de secuencias")
            
            # ⭐⭐ NUEVO: Generar reporte de confirmados por mes ⭐⭐
            print("\n📈 Generando reporte de confirmados por mes...")
            reporte_confirmados = ReportService.generar_reporte_confirmados_por_mes(db, "cantidad_confirmados_por_mes.xlsx")
            
            if reporte_confirmados:
                print("✅ Reporte de confirmados por mes exportado exitosamente")
            else:
                print("⚠️ No se pudo exportar el reporte de confirmados por mes")
            
            # ⭐⭐ NUEVO: Generar reporte de presupuesto de becas ⭐⭐
            print("\n💰 Generando reporte de presupuesto de becas...")
            reporte_presupuesto = ReportService.generar_reporte_presupuesto_becas(db, "presupuesto_becas.xlsx")
            
            if reporte_presupuesto:
                print("✅ Reporte de presupuesto de becas exportado exitosamente")
                print("📊 Contenido del archivo:")
                print("   - Hoja 'Presupuesto': Datos detallados de presupuesto")
                print("   - Gráfico: Comparación gasto real vs planeado y excedente acumulado")
            else:
                print("⚠️ No se pudo exportar el reporte de presupuesto de becas")
        
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