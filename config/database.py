# config/database.py - AGREGAR AL PRINCIPIO
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import MySQLConfig

# DEBUG: Verificar la configuración
MySQLConfig.print_config()

# Validar que no sean None
if not all([MySQLConfig.HOST, MySQLConfig.USER, MySQLConfig.PASSWORD, MySQLConfig.DB]):
    raise ValueError("❌ Faltan variables de configuración MySQL")

MySQLConfig.validate()

# Cargar variables de entorno desde .env
load_dotenv()
# Configuración de la conexión desde settings.py
DB_CONFIG = {
    'host': MySQLConfig.HOST,
    'user': MySQLConfig.USER,
    'password': MySQLConfig.PASSWORD,
    'database': MySQLConfig.DB,
    'port': 3306
}

# Crear la cadena de conexión
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, 
                      echo=False,
                      pool_size=10,
                      max_overflow=20,
                      pool_recycle=3600,
                      connect_args={'connect_timeout': 30})

# Crear sesión ← ¡ESTA LÍNEA FALTA!
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar la conexión
def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Conexión exitosa a la base de datos")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False