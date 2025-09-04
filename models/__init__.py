# models/__init__.py

# Importar desde los nuevos submódulos
from .orm.models import (
    Formulario,
    FormularioOferta,
    Adolescente,
    DatosPersonales,
    OfertaActividad,
    Actividad,
    Sede,
    Dia,
    OfertaDia
)

from .reports.vista_oferta import VistaOferta

# Opcional: también puedes hacer available los modelos directamente
__all__ = [
    'Formulario',
    'FormularioOferta', 
    'Adolescente',
    'DatosPersonales',
    'OfertaActividad',
    'Actividad',
    'Sede',
    'Dia',
    'OfertaDia',
    'VistaOferta'
]