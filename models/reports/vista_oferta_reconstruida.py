# models/reports/vista_oferta_reconstruida.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import List, TYPE_CHECKING
from datetime import datetime

# Importar el modificador específico
from .modificador_registros_agrega_02_antes_que_04 import agregar_registros_02_antes_que_04
from .modificador_registros_agrega_02_antes_que_05 import agregar_registros_02_antes_que_05

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
    
    # ⭐⭐ NUEVO CAMPO: Para identificar registros agregados por modificadores ⭐⭐
    registro_agregado = Column(String(100), nullable=True)
    
    # ⭐⭐ NUEVO CAMPO: Para almacenar los meses en el programa ⭐⭐
    meses_en_el_programa = Column(String(500), nullable=True)
    
    # ⭐⭐ NUEVOS CAMPOS: Para almacenar la presencia en cada mes ⭐⭐
    enero = Column(Integer, default=0, nullable=True)
    febrero = Column(Integer, default=0, nullable=True)
    marzo = Column(Integer, default=0, nullable=True)
    abril = Column(Integer, default=0, nullable=True)
    mayo = Column(Integer, default=0, nullable=True)
    junio = Column(Integer, default=0, nullable=True)
    julio = Column(Integer, default=0, nullable=True)
    agosto = Column(Integer, default=0, nullable=True)
    septiembre = Column(Integer, default=0, nullable=True)
    octubre = Column(Integer, default=0, nullable=True)
    noviembre = Column(Integer, default=0, nullable=True)
    diciembre = Column(Integer, default=0, nullable=True)
    
# models/reports/vista_oferta_reconstruida.py
    def __init__(self, vista_original: 'VistaOferta' = None, **kwargs):
        """
        Constructor que permite crear una instancia a partir de VistaOferta original
        o mediante parámetros con nombre
        """
        if vista_original:
            self._mapear_desde_vista_original(vista_original)
        elif kwargs:
            # Establecer atributos directamente desde kwargs
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
    
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
# models/reports/vista_oferta_reconstruida.py
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# ... (código existente de la clase VistaOfertaReconstruida)

def convertir_vistas_reconstruidas(datos_crudos: list) -> List[VistaOfertaReconstruida]:
    """
    Convierte los datos crudos de VistaOferta a VistaOfertaReconstruida
    con ordenamiento especial para casos con misma fecha updated_at
    """
    # Agrupar por formulario_id
    formularios = {}
    for dato in datos_crudos:
        if dato.formulario_id not in formularios:
            formularios[dato.formulario_id] = []
        formularios[dato.formulario_id].append(dato)
    
    resultados = []
    
    # Procesar cada formulario
    for formulario_id, registros in formularios.items():
        # Ordenar con múltiples criterios
        registros_ordenados = sorted(
            registros, 
            key=lambda x: (
                x.updated_at, 
                # Criterio 1: Priorizar (0,0) sobre otros
                0 if (x.asignada == False and x.estado == 0) else 1,
                # Criterio 2: Para registros con mismas fechas, priorizar (0,1) sobre (0,5)
                # Asignamos valores: (0,1) -> 0, (0,5) -> 1, otros -> 2
                0 if (x.asignada == False and x.estado == 1) else (
                    1 if (x.asignada == False and x.estado == 5) else 2
                ),
                # Mantener orden original para otros casos
                x.created_at,
                x.estado
            )
        )
        
        # Convertir a VistaOfertaReconstruida usando el mapeo desde vista_original
        for registro in registros_ordenados:
            obj = VistaOfertaReconstruida()
            obj._mapear_desde_vista_original(registro)
            resultados.append(obj)
    
    # ⭐⭐ APLICAR MODIFICADORES ESPECÍFICOS ⭐⭐
    # Importar aquí para evitar circular import
    from .modificador_registros_agrega_02_antes_que_04 import agregar_registros_02_antes_que_04
    from .modificador_registros_agrega_02_antes_que_05 import agregar_registros_02_antes_que_05
    
    resultados = agregar_registros_02_antes_que_04(resultados)
    resultados = agregar_registros_02_antes_que_05(resultados)
    
    # ⭐⭐ CALCULAR MESES EN EL PROGRAMA ⭐⭐
    from .modificador_registros_agrega_campo_meses_en_el_programa import calcular_meses_en_programa
    resultados = calcular_meses_en_programa(resultados)
    
    return resultados
