from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class VistaOferta(Base):
    """
    Modelo para la vista vista_oferta - Optimizado para reportes
    """
    __tablename__ = 'vista_oferta'
    
    # Columnas de la vista
    id_adolescente = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    dni = Column(String(20))  # Se mapea automáticamente a 'DNI' en la BD
    sede = Column(String(100))
    actividad = Column(String(100))
    dia = Column(String(50))
    horario = Column(String(50))
    
    # Campos de formulario_oferta
    id = Column(Integer, primary_key=True)  # ID de formulario_oferta
    formulario_id = Column(Integer)
    oferta_actividad_id = Column(Integer)
    asignada = Column(Boolean)
    estado = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Campo de formularios
    confirmado = Column(Boolean)
    
    def __repr__(self):
        return f"<VistaOferta {self.dni} - {self.nombre} {self.apellido}>"
    
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
    
    @property
    def mes_anio(self):
        """Para agrupar por mes fácilmente"""
        if self.updated_at:
            return self.updated_at.strftime('%Y-%m')
        return None