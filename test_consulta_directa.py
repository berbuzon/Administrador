# test_consulta_directa.py
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
import os

# Conexión directa
engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}")

try:
    with engine.connect() as conn:
        # Consulta directa similar a lo que hace tu ReportService
        query = text("""
            SELECT 
                YEAR(updated_at) as ano,
                MONTH(updated_at) as mes,
                COUNT(DISTINCT id_adolescente) as total_adolescentes
            FROM vista_oferta 
            WHERE confirmado = 1 
                AND asignada = 1 
                AND estado = 2
                AND updated_at >= '2025-03-17'
            GROUP BY YEAR(updated_at), MONTH(updated_at)
            ORDER BY ano, mes
        """)
        
        result = conn.execute(query)
        resultados = result.all()
        
        print("📊 Resultados de consulta directa:")
        print(f"{'Año':<6} {'Mes':<6} {'Total':<8}")
        print("-" * 20)
        
        for ano, mes, total in resultados:
            print(f"{ano:<6} {mes:<6} {total:<8}")
            
        print(f"✅ Total de meses: {len(resultados)}")
        
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()