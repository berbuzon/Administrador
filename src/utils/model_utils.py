import pandas as pd
from sqlalchemy.orm import Session

class ModelUtils:
    """Utilidades para trabajar con modelos SQLAlchemy y convertirlos a DataFrames"""
    
    @staticmethod
    def model_to_dataframe(session: Session, model_class):
        """
        Convierte todos los registros de un modelo SQLAlchemy a DataFrame
        
        Args:
            session: Sesión de SQLAlchemy  
            model_class: Clase del modelo SQLAlchemy
            
        Returns:
            DataFrame con todos los registros de la tabla
        """
        query = session.query(model_class)
        return pd.read_sql(query.statement, session.bind)