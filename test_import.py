# test_imports.py
print("1. Importando config.database...")
try:
    from config.database import test_connection
    print("✅ config.database importado")
    
    print("2. Probando conexión...")
    if test_connection():
        print("✅ Conexión exitosa")
    else:
        print("❌ Conexión falló")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

input("Presiona Enter...")