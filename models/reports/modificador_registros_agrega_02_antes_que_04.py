# models/reports/modificador_registros_agrega_02_antes_que_04.py
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida

def agregar_registros_02_antes_que_04(registros: List['VistaOfertaReconstruida']) -> List['VistaOfertaReconstruida']:
    """
    Agrega registros intermedios con estado=2 antes de registros con asignada=0 y estado=4.
    """
    # Importar aquí para evitar circular import
    from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida
    
    nuevos_registros = []
    
    for i, registro in enumerate(registros):
        # Verificar si cumple el criterio: asignada=0 y estado=4
        if registro.asignada == False and registro.estado == 4:
            # Crear un nuevo registro intermedio
            nuevo_registro = VistaOfertaReconstruida()
            
            # Copiar todos los campos del registro actual
            for attr in ['id_adolescente', 'Nombre', 'Apellido', 'DNI', 'Sede', 
                         'Actividad', 'Dia', 'Horario', 'formulario_id', 
                         'oferta_actividad_id', 'asignada', 'confirmado']:
                setattr(nuevo_registro, attr, getattr(registro, attr))
            
            # Modificar campos según criterio
            nuevo_registro.estado = 2
            
            # Buscar el registro anterior para el mismo formulario_id
            registro_anterior = None
            for j in range(i-1, -1, -1):
                if registros[j].formulario_id == registro.formulario_id:
                    registro_anterior = registros[j]
                    break
            
            # Establecer fechas según criterio
            if registro_anterior:
                nuevo_registro.created_at = registro_anterior.updated_at
            else:
                nuevo_registro.created_at = registro.created_at
                
            nuevo_registro.updated_at = registro.created_at
            
            # ⭐⭐ ESTABLECER EL CAMPO DE REGISTRO AGREGADO ⭐⭐
            nuevo_registro.registro_agregado = "agregar_registros_02_antes_que_04"
            
            # Agregar el nuevo registro a la lista
            nuevos_registros.append(nuevo_registro)
        
        # Siempre agregar el registro original
        nuevos_registros.append(registro)
    
    return nuevos_registros