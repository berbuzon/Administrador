# config/settings.py
from os import getenv
from dotenv import load_dotenv

# Cargar variables de entorno PRIMERO
load_dotenv()

class MySQLConfig:
    HOST = getenv('MYSQL_HOST')
    USER = getenv('MYSQL_USER')
    PASSWORD = getenv('MYSQL_PASSWORD')
    DB = getenv('MYSQL_DB')
    
    # Método para verificar
    @classmethod
    def print_config(cls):
        print("🔧 Configuración MySQL:")
        print(f"   HOST: {cls.HOST}")
        print(f"   USER: {cls.USER}")
        print(f"   DB: {cls.DB}")
        print(f"   PASSWORD: {'*' * len(cls.PASSWORD) if cls.PASSWORD else 'None'}")
    
    # Método para validar (AGREGA ESTO)
    @classmethod
    def validate(cls):
        missing = []
        if not cls.HOST: missing.append('MYSQL_HOST')
        if not cls.USER: missing.append('MYSQL_USER')
        if not cls.PASSWORD: missing.append('MYSQL_PASSWORD')
        if not cls.DB: missing.append('MYSQL_DB')
        
        if missing:
            raise ValueError(f"Faltan variables de entorno: {missing}")