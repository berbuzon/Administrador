import pandas as pd
from sqlalchemy.orm import Session

class QueryUtils:
    """Utilidades para trabajar con queries SQL directos y convertirlos a DataFrames"""
    
    @staticmethod
    def query_to_dataframe(session: Session, query, params=None):
        """
        Ejecuta un query SQL directo y devuelve un DataFrame
        
        Args:
            session: Sesión de SQLAlchemy
            query: Query SQL como string
            params: Parámetros para el query (opcional)
            
        Returns:
            DataFrame con los resultados del query
        """
        return pd.read_sql(query, session.bind, params=params)