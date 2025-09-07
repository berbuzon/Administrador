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

    # Agrupar registros por formulario_id
    formularios = {}
    for registro in registros:
        if registro.formulario_id not in formularios:
            formularios[registro.formulario_id] = []
        formularios[registro.formulario_id].append(registro)

    nuevos_registros = []
    
    for formulario_id, registros_formulario in formularios.items():
        # Verificar si el primer registro es (0,5)
        primer_registro = registros_formulario[0]
        es_primer_registro_05 = (primer_registro.asignada == False and primer_registro.estado == 5)
        
        if es_primer_registro_05:
            # Caso 1: Primer registro es (0,5)
            nuevo_registro = VistaOfertaReconstruida()
            
            # Copiar todos los campos del primer registro
            for attr in ['id_adolescente', 'Nombre', 'Apellido', 'DNI', 'Sede', 
                         'Actividad', 'Dia', 'Horario', 'formulario_id', 
                         'oferta_actividad_id', 'asignada', 'confirmado']:
                setattr(nuevo_registro, attr, getattr(primer_registro, attr))
            
            # Modificar estado a 2
            nuevo_registro.estado = 2
            
            # ⭐⭐ CORRECCIÓN: created_at del nuevo registro = created_at del registro (0,5)
            nuevo_registro.created_at = primer_registro.created_at
            # updated_at del nuevo registro = updated_at del registro (0,5)
            nuevo_registro.updated_at = primer_registro.updated_at
            
            nuevo_registro.registro_agregado = "agregar_registros_02_antes_que_05"
            
            # Insertar el nuevo registro al principio
            nuevos_registros.append(nuevo_registro)
            
            # Agregar todos los registros del formulario
            nuevos_registros.extend(registros_formulario)
        else:
            # Caso 2: El primer registro no es (0,5)
            # Buscar registros (0,5) en el formulario
            for i, registro in enumerate(registros_formulario):
                if registro.asignada == False and registro.estado == 5:
                    # Encontrar el registro anterior (inmediatamente superior)
                    registro_anterior = None
                    if i > 0:
                        registro_anterior = registros_formulario[i-1]
                    
                    # Crear nuevo registro (0,2)
                    nuevo_registro = VistaOfertaReconstruida()
                    
                    # Copiar todos los campos del registro actual (0,5)
                    for attr in ['id_adolescente', 'Nombre', 'Apellido', 'DNI', 'Sede', 
                                 'Actividad', 'Dia', 'Horario', 'formulario_id', 
                                 'oferta_actividad_id', 'asignada', 'confirmado']:
                        setattr(nuevo_registro, attr, getattr(registro, attr))
                    
                    # Modificar campos según criterio
                    nuevo_registro.estado = 2
                    
                    # ⭐⭐ CORRECCIÓN: created_at del nuevo registro = updated_at del registro anterior
                    if registro_anterior:
                        nuevo_registro.created_at = registro_anterior.updated_at
                    else:
                        nuevo_registro.created_at = registro.created_at
                    
                    # updated_at del nuevo registro = updated_at del registro (0,5)
                    nuevo_registro.updated_at = registro.updated_at
                    
                    nuevo_registro.registro_agregado = "agregar_registros_02_antes_que_05"
                    
                    # Modificar el registro (0,5) original: created_at = updated_at (original)
                    registro_original_updated_at = registro.updated_at
                    registro.created_at = registro_original_updated_at
                    
                    # Agregar el nuevo registro antes del registro (0,5)
                    nuevos_registros.append(nuevo_registro)
                    nuevos_registros.append(registro)
                else:
                    # Agregar registros que no son (0,5) sin cambios
                    nuevos_registros.append(registro)
    
    return nuevos_registros