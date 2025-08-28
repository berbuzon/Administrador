# main_funcional.py
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from datetime import datetime

# Configuración de conexión
engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}")
SessionLocal = sessionmaker(bind=engine)

def main():
    print("📊 Generando reporte desde vista_oferta...")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Consulta que sabemos funciona
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
        
        result = db.execute(query)
        resultados = result.all()
        
        if not resultados:
            print("ℹ️ No se encontraron resultados")
            return
        
        print("\n📈 ADOLESCENTES ACEPTADOS POR MES")
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
        
        # Exportar a Excel
        df = pd.DataFrame(resultados, columns=['año', 'mes', 'total_adolescentes'])
        df['mes_nombre'] = df['mes'].apply(lambda x: datetime(2023, x, 1).strftime('%B'))
        df['periodo'] = df['año'].astype(str) + '-' + df['mes'].astype(str).str.zfill(2)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_aceptados_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        print(f"\n💾 Reporte exportado: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
        print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    main()