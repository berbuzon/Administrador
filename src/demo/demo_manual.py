from src.utils.model_utils import ModelUtils
from src.database.models_manual import RazonSocial, Institucion

def demostrar_modelos_manuales(session_sql, session_mysql):
    """Demuestra el uso de modelos definidos manualmente"""
    print("\n" + "="*50)
    print("🧠 ENFOQUE MANUAL: Modelos definidos a mano")
    print("="*50)
    
    # 1. Usar modelos manuales
    print("\n=== Datos usando Modelos Manuales ===")
    razones_sociales = session_sql.query(RazonSocial).limit(3).all()
    for rs in razones_sociales:
        print(f"ID: {rs.id}, Razón Social: {rs.RazonSocial}")

    # 2. Usar Pandas con modelos manuales
    print("\n=== DataFrame desde Modelos Manuales ===")
    df_instituciones = ModelUtils.model_to_dataframe(session_mysql, Institucion)
    print(df_instituciones.head(3))