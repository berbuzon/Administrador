# models/reports/vista_oferta_reconstruida.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class VistaOfertaReconstruida(Base):
    """
    Modelo reconstruido para la vista vista_oferta - Estructura mejorada y organizada
    """
    __tablename__ = 'vista_oferta_reconstruida'
    
    # ID principal (puede ser el mismo id de formulario_oferta o crear uno nuevo)
    id = Column(Integer, primary_key=True)
    
    # Información del adolescente (agrupada y con nombres más claros)
    adolescente_id = Column(Integer)
    nombre_adolescente = Column(String(100))
    apellido_adolescente = Column(String(100))
    dni_adolescente = Column(String(20))
    
    # Información de la oferta/sede (agrupada)
    sede_nombre = Column(String(100))
    actividad_nombre = Column(String(100))
    dia_semana = Column(String(50))
    horario_actividad = Column(String(50))
    
    # Información del formulario (agrupada)
    formulario_id = Column(Integer)
    oferta_actividad_id = Column(Integer)
    
    # Estados y flags (nombres más descriptivos)
    oferta_asignada = Column(Boolean)
    estado_oferta = Column(Integer)
    formulario_confirmado = Column(Boolean)
    
    # Timestamps
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)
    
    def __init__(self, vista_original: 'VistaOferta' = None):
        """
        Constructor que permite crear una instancia a partir de VistaOferta original
        """
        if vista_original:
            self._mapear_desde_vista_original(vista_original)
    
    def _mapear_desde_vista_original(self, vista_original: 'VistaOferta'):
        """Mapea los datos desde la vista original"""
        # Información del adolescente
        self.adolescente_id = vista_original.id_adolescente
        self.nombre_adolescente = vista_original.Nombre
        self.apellido_adolescente = vista_original.Apellido
        self.dni_adolescente = vista_original.DNI
        
        # Información de la oferta
        self.sede_nombre = vista_original.Sede
        self.actividad_nombre = vista_original.Actividad
        self.dia_semana = vista_original.Dia
        self.horario_actividad = vista_original.Horario
        
        # Información del formulario
        self.formulario_id = vista_original.formulario_id
        self.oferta_actividad_id = vista_original.oferta_actividad_id
        self.id = vista_original.id
        
        # Estados
        self.oferta_asignada = vista_original.asignada
        self.estado_oferta = vista_original.estado
        self.formulario_confirmado = vista_original.confirmado
        
        # Timestamps
        self.fecha_creacion = vista_original.created_at
        self.fecha_actualizacion = vista_original.updated_at
    
    def __repr__(self):
        return f"<VistaOfertaReconstruida {self.dni_adolescente} - {self.nombre_adolescente} {self.apellido_adolescente}>"
    
    @property
    def estado_texto(self):
        estados = {
            0: 'Sin datos', 1: 'Pendiente', 2: 'Aceptado',
            3: 'Sin datos', 4: 'Cambio', 5: 'Baja'
        }
        return estados.get(self.estado_oferta, 'Desconocido')
    
    @property
    def asignada_texto(self):
        return 'Asignada' if self.oferta_asignada else 'No asignada'
    
    @property
    def confirmado_texto(self):
        return 'Confirmado' if self.formulario_confirmado else 'No confirmado'
    
    @property
    def nombre_completo(self):
        return f"{self.nombre_adolescente} {self.apellido_adolescente}"
    
    @property
    def actividad_completa(self):
        return f"{self.actividad_nombre} - {self.dia_semana} {self.horario_actividad}"
    
    def to_dict(self):
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            'id': self.id,
            'adolescente_id': self.adolescente_id,
            'nombre_completo': self.nombre_completo,
            'dni': self.dni_adolescente,
            'sede': self.sede_nombre,
            'actividad': self.actividad_completa,
            'dia': self.dia_semana,
            'horario': self.horario_actividad,
            'asignada': self.oferta_asignada,
            'asignada_texto': self.asignada_texto,
            'estado': self.estado_oferta,
            'estado_texto': self.estado_texto,
            'confirmado': self.formulario_confirmado,
            'confirmado_texto': self.confirmado_texto,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion
        }


# Función utilitaria para convertir múltiples objetos
def convertir_vistas_reconstruidas(vistas_originales: list) -> list[VistaOfertaReconstruida]:
    """
    Convierte una lista de VistaOferta a VistaOfertaReconstruida
    """
    return [VistaOfertaReconstruida(vista) for vista in vistas_originales]