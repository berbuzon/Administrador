# models/reports/vista_oferta_reconstruida.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class VistaOfertaReconstruida(Base):
    """
    Modelo reconstruido para la vista vista_oferta - Mismos nombres que VistaOferta
    """
    __tablename__ = 'vista_oferta_reconstruida'
    
    # Columnas principales (mismos nombres que VistaOferta)
    id_adolescente = Column(Integer, primary_key=True)
    Nombre = Column(String(100))
    Apellido = Column(String(100))
    DNI = Column(String(20))
    Sede = Column(String(100))
    Actividad = Column(String(100))
    Dia = Column(String(50))
    Horario = Column(String(50))
    
    # Campos de formulario_oferta (mismos nombres)
    id = Column(Integer)
    formulario_id = Column(Integer)
    oferta_actividad_id = Column(Integer)
    asignada = Column(Boolean)
    estado = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Campo de formularios (mismo nombre)
    confirmado = Column(Boolean)
    
    def __init__(self, vista_original: 'VistaOferta' = None):
        """
        Constructor que permite crear una instancia a partir de VistaOferta original
        """
        if vista_original:
            self._mapear_desde_vista_original(vista_original)
    
    def _mapear_desde_vista_original(self, vista_original: 'VistaOferta'):
        """Mapea los datos desde la vista original"""
        # Información del adolescente
        self.id_adolescente = vista_original.id_adolescente
        self.Nombre = vista_original.Nombre
        self.Apellido = vista_original.Apellido
        self.DNI = vista_original.DNI
        
        # Información de la oferta
        self.Sede = vista_original.Sede
        self.Actividad = vista_original.Actividad
        self.Dia = vista_original.Dia
        self.Horario = vista_original.Horario
        
        # Información del formulario
        self.formulario_id = vista_original.formulario_id
        self.oferta_actividad_id = vista_original.oferta_actividad_id
        self.id = vista_original.id
        
        # Estados
        self.asignada = vista_original.asignada
        self.estado = vista_original.estado
        self.confirmado = vista_original.confirmado
        
        # Timestamps
        self.created_at = vista_original.created_at
        self.updated_at = vista_original.updated_at
    
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
    def nombre_completo(self):
        return f"{self.Nombre} {self.Apellido}"
    
    @property
    def actividad_completa(self):
        return f"{self.Actividad} - {self.Dia} {self.Horario}"


# Función utilitaria para convertir múltiples objetos
def convertir_vistas_reconstruidas(vistas_originales: list) -> list[VistaOfertaReconstruida]:
    """
    Convierte una lista de VistaOferta a VistaOfertaReconstruida
    """
    return [VistaOfertaReconstruida(vista) for vista in vistas_originales]