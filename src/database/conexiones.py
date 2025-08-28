from sqlalchemy import create_engine
from config.settings import MySQLConfig
# from sqlalchemy import text  # Necesario para ejecutar queries

def conectar_mysql():
    # Conexión MySQL con parámetros optimizados
    engine = create_engine(
        f"mysql+pymysql://{MySQLConfig.USER}:{MySQLConfig.PASSWORD}@{MySQLConfig.HOST}/{MySQLConfig.DB}",
        pool_size=5,
        pool_recycle=3600,
        connect_args={
            'connect_timeout': 10,
            'charset': 'utf8mb4'
        }
    )
    return engine
