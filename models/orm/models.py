from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class Formulario(Base):
    __tablename__ = 'formularios'
    
    id = Column(Integer, primary_key=True, index=True)
    id_adolescente = Column(Integer, index=True)
    confirmado = Column(Boolean, default=False)
    fecha_confirmacion = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    ofertas = relationship("FormularioOferta", back_populates="formulario")
    adolescente = relationship("Adolescente", back_populates="formularios", foreign_keys=[id_adolescente])
    
    def __repr__(self):
        return f"<Formulario {self.id} - Adolescente: {self.id_adolescente}>"

class FormularioOferta(Base):
    __tablename__ = 'formulario_oferta'
    
    id = Column(Integer, primary_key=True, index=True)
    formulario_id = Column(Integer, ForeignKey('formularios.id'), index=True)
    oferta_actividad_id = Column(Integer, ForeignKey('ofertas_actividades.id'), index=True)
    asignada = Column(Boolean, default=False)
    estado = Column(Integer)  # 0-5 según tu descripción
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    formulario = relationship("Formulario", back_populates="ofertas")
    oferta_actividad = relationship("OfertaActividad", back_populates="formularios_oferta")
    
    def __repr__(self):
        return f"<FormularioOferta {self.id} - Estado: {self.estado}>"
    
    @property
    def estado_texto(self):
        """Devuelve el texto del estado"""
        estados = {
            0: 'Sin datos',
            1: 'Pendiente', 
            2: 'Aceptado',
            3: 'Sin datos',
            4: 'Cambio de actividad',
            5: 'Baja de actividad'
        }
        return estados.get(self.estado, 'Desconocido')
    
    @property
    def asignada_texto(self):
        """Devuelve el texto de asignada"""
        return 'Asignada' if self.asignada else 'No asignada'

class Adolescente(Base):
    __tablename__ = 'adolescentes'
    
    id = Column(Integer, primary_key=True, index=True)
    id_datos_personales = Column(Integer, ForeignKey('datos_personales.id'), index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    datos_personales = relationship("DatosPersonales", back_populates="adolescentes")
    formularios = relationship("Formulario", back_populates="adolescente", foreign_keys=[Formulario.id_adolescente])
    
    def __repr__(self):
        return f"<Adolescente {self.id}>"

class DatosPersonales(Base):
    __tablename__ = 'datos_personales'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    numero_doc = Column(String(20), index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    adolescentes = relationship("Adolescente", back_populates="datos_personales")
    
    def __repr__(self):
        return f"<DatosPersonales {self.nombre} {self.apellido}>"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class OfertaActividad(Base):
    __tablename__ = 'ofertas_actividades'
    
    id = Column(Integer, primary_key=True, index=True)
    actividad_id = Column(Integer, ForeignKey('actividades.id'), index=True)
    sede_id = Column(Integer, ForeignKey('sedes.id'), index=True)
    horario = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    actividad = relationship("Actividad", back_populates="ofertas")
    sede = relationship("Sede", back_populates="ofertas")
    formularios_oferta = relationship("FormularioOferta", back_populates="oferta_actividad")
    dias = relationship("Dia", secondary="oferta_dia", back_populates="ofertas")
    
    def __repr__(self):
        return f"<OfertaActividad {self.id}>"

class Actividad(Base):
    __tablename__ = 'actividades'
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    ofertas = relationship("OfertaActividad", back_populates="actividad")
    
    def __repr__(self):
        return f"<Actividad {self.valor}>"

class Sede(Base):
    __tablename__ = 'sedes'
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    ofertas = relationship("OfertaActividad", back_populates="sede")
    
    def __repr__(self):
        return f"<Sede {self.valor}>"

class Dia(Base):
    __tablename__ = 'dias'
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relación muchos-a-muchos con OfertaActividad
    ofertas = relationship("OfertaActividad", secondary="oferta_dia", back_populates="dias")
    
    def __repr__(self):
        return f"<Dia {self.valor}>"

# Tabla intermedia para relación muchos-a-muchos
class OfertaDia(Base):
    __tablename__ = 'oferta_dia'
    
    id = Column(Integer, primary_key=True, index=True)
    oferta_id = Column(Integer, ForeignKey('ofertas_actividades.id'), index=True)
    dia_id = Column(Integer, ForeignKey('dias.id'), index=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<OfertaDia Oferta:{self.oferta_id} - Dia:{self.dia_id}>"