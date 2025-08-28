import pandas as pd
from sqlalchemy.orm import Session

class StorageUtils:
    """Utilidades para guardar DataFrames en la base de datos"""
    
    @staticmethod
    def dataframe_to_database(df, table_name, session, if_exists='append'):
        """
        Guarda un DataFrame en la base de datos
        
        Args:
            df: DataFrame a guardar
            table_name: Nombre de la tabla destino
            session: Sesión de SQLAlchemy
            if_exists: Comportamiento si la tabla existe ('fail', 'replace', 'append')
        """
        df.to_sql(
            table_name,
            session.bind,
            if_exists=if_exists,
            index=False
        )