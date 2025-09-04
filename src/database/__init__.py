# src/database/__init__.py
from .conexiones import conectar_mysql
# from .models_manual import VistaOferta

__all__ = ['conectar_mysql', 'VistaOferta']