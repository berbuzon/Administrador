# test_vista.py
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Conexión directa
engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}")

try:
    with engine.connect() as conn:
        # Verificar si la vista existe
        result = conn.execute(text("SELECT COUNT(*) FROM information_schema.views WHERE table_name = 'vista_oferta'"))
        vista_existe = result.scalar()
        print(f'✅ Vista existe: {vista_existe > 0}')
        
        if vista_existe:
            # Contar registros en la vista
            result = conn.execute(text("SELECT COUNT(*) FROM vista_oferta"))
            count = result.scalar()
            print(f'✅ Registros en vista: {count}')
            
            # Verificar algunos registros de muestra
            result = conn.execute(text("SELECT * FROM vista_oferta LIMIT 5"))
            for row in result:
                print(f'📋 Muestra: {row}')
                
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()