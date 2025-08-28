# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print("🔍 Verificando variables de entorno:")
print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
print(f"MYSQL_DB: {os.getenv('MYSQL_DB')}")
print(f"MYSQL_PASSWORD: {'*' * len(os.getenv('MYSQL_PASSWORD', ''))}")

input("Presiona Enter...")