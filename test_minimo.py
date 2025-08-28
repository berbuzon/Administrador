# test_minimo.py
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Conexión directa
engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}")

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Conexión exitosa')
except Exception as e:
    print(f'❌ Error de conexión: {e}')