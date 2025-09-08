# models/reports/modificador_registros_agrega_02_antes_que_05.py
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida

def agregar_registros_02_antes_que_05(registros: List['VistaOfertaReconstruida']) -> List['VistaOfertaReconstruida']:
    """
    Agrega registros con estado=2 antes de registros con estado=5 según criterios específicos.
    """
    # Importar aquí para evitar circular import
    from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida

    nuevos_registros = []
    
    for registro in registros:
        if registro.asignada == False and registro.estado == 5:
            # Crear nuevo registro (0,2)
            nuevo_registro = VistaOfertaReconstruida()
            
            # Copiar todos los campos del registro actual (0,5)
            for attr in ['id_adolescente', 'Nombre', 'Apellido', 'DNI', 'Sede', 
                         'Actividad', 'Dia', 'Horario', 'formulario_id', 
                         'oferta_actividad_id', 'asignada', 'confirmado',
                         'created_at', 'updated_at']:
                setattr(nuevo_registro, attr, getattr(registro, attr))
            
            # Modificar estado a 2
            nuevo_registro.estado = 2
            nuevo_registro.registro_agregado = "agregar_registros_02_antes_que_05"
            
            # ⭐⭐ MODIFICACIÓN: Actualizar created_at del registro original (0,5) a su updated_at
            registro_original_updated_at = registro.updated_at
            registro.created_at = registro_original_updated_at
            
            # Agregar el nuevo registro antes del registro (0,5)
            nuevos_registros.append(nuevo_registro)
            nuevos_registros.append(registro)
        else:
            # Agregar registros que no son (0,5) sin cambios
            nuevos_registros.append(registro)
    
    return nuevos_registros