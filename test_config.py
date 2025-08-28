# test_config.py
from config.settings import MySQLConfig

print("🔍 Configuración desde MySQLConfig:")
print(f"HOST: {MySQLConfig.HOST}")
print(f"USER: {MySQLConfig.USER}")
print(f"DB: {MySQLConfig.DB}")
print(f"PASSWORD: {'*' * len(MySQLConfig.PASSWORD) if MySQLConfig.PASSWORD else 'None'}")

input("Presiona Enter...")
