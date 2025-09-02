from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class VistaOferta(Base):
    """
    Modelo para la vista vista_oferta - Optimizado para reportes
    """
    __tablename__ = 'vista_oferta'
    
    # Columnas principales (deben coincidir exactamente con la vista)
    id_adolescente = Column(Integer, primary_key=True)
    Nombre = Column(String(100))  # Exactamente como en la vista
    Apellido = Column(String(100))  # Exactamente como en la vista
    DNI = Column(String(20))  # Exactamente como en la vista
    Sede = Column(String(100))  # Exactamente como en la vista
    Actividad = Column(String(100))  # Exactamente como en la vista
    Dia = Column(String(50))  # Exactamente como en la vista
    Horario = Column(String(50))  # Exactamente como en la vista
    
    # Campos de formulario_oferta (deben coincidir exactamente)
    id = Column(Integer, primary_key=True)  # ID de formulario_oferta
    formulario_id = Column(Integer)
    oferta_actividad_id = Column(Integer)
    asignada = Column(Boolean)
    estado = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Campo de formularios (debe coincidir exactamente)
    confirmado = Column(Boolean)
    
    def __repr__(self):
        return f"<VistaOferta {self.DNI} - {self.Nombre} {self.Apellido}>"
    
    @property
    def estado_texto(self):
        estados = {
            0: 'Sin datos', 1: 'Pendiente', 2: 'Aceptado',
            3: 'Sin datos', 4: 'Cambio', 5: 'Baja'
        }
        return estados.get(self.estado, 'Desconocido')
    
    @property
    def asignada_texto(self):
        return 'Asignada' if self.asignada else 'No asignada'
    
    @property
    def confirmado_texto(self):
        return 'Confirmado' if self.confirmado else 'No confirmado'
