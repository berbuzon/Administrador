# test_report_service.py
from config.database import SessionLocal
from services.report_service import ReportService

db = SessionLocal()
try:
    print("Testing ReportService...")
    resultados = ReportService.get_adolescentes_aceptados_por_mes_vista(db)
    print(f"✅ Resultados: {len(resultados)} meses encontrados")
except Exception as e:
    print(f"❌ Error en ReportService: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()