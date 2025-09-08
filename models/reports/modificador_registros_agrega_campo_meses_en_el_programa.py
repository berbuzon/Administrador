# models/reports/modificador_registros_agrega_campo_meses_en_el_programa.py
from datetime import datetime
from typing import List
from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida

def calcular_meses_en_programa(registros: List[VistaOfertaReconstruida]) -> List[VistaOfertaReconstruida]:
    """
    Calcula y agrega el campo 'meses_en_el_programa' a los registros con estado=2
    según los criterios especificados.
    """
    
    # ⭐⭐ DEFINIR meses_objetivo ANTES DE USARLA ⭐⭐
    meses_objetivo = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                      "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    # Agrupar registros por formulario_id
    formularios = {}
    for registro in registros:
        if registro.formulario_id not in formularios:
            formularios[registro.formulario_id] = []
        formularios[registro.formulario_id].append(registro)
    
    # Ordenar cada formulario por updated_at
    for formulario_id, registros_formulario in formularios.items():
        registros_formulario.sort(key=lambda x: x.updated_at)
    
    # Meses en español
    meses_es = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    
    # Obtener mes actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    # Procesar cada formulario
    for formulario_id, registros_formulario in formularios.items():
        # Ordenar registros por updated_at para asegurar el orden correcto
        registros_formulario.sort(key=lambda x: x.updated_at)
        
        # Encontrar todos los registros con estado=2 en este formulario
        registros_estado_2 = [r for r in registros_formulario if r.estado == 2]
        
        for registro_estado_2 in registros_estado_2:
            # Fecha de inicio (created_at del registro estado=2)
            fecha_inicio = registro_estado_2.created_at
            
            # Encontrar la posición de este registro en la lista ordenada
            posicion_actual = None
            for i, registro in enumerate(registros_formulario):
                if registro.updated_at == registro_estado_2.updated_at and registro.estado == registro_estado_2.estado:
                    posicion_actual = i
                    break
            
            # Buscar el primer registro posterior con estado=4 o estado=5
            fecha_fin = None
            if posicion_actual is not None:
                for i in range(posicion_actual + 1, len(registros_formulario)):
                    registro = registros_formulario[i]
                    if registro.estado in [4, 5]:
                        fecha_fin = registro.updated_at
                        break
            
            # Si no hay registro posterior con estado=4 o 5, usar el mes actual
            if fecha_fin is None:
                fecha_fin = datetime(año_actual, mes_actual, 1)
            else:
                # Asegurar que fecha_fin sea un objeto datetime
                if isinstance(fecha_fin, str):
                    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d %H:%M:%S")
            
            # Calcular los meses entre fecha_inicio y fecha_fin
            meses_en_programa = []
            
            # Convertir a objetos datetime si es necesario
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d %H:%M:%S")
            
            # Comenzar desde el mes de inicio
            current_month = fecha_inicio.month
            current_year = fecha_inicio.year
            
            # Terminar en el mes de fin
            end_month = fecha_fin.month
            end_year = fecha_fin.year
            
            # Calcular los meses
            while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
                meses_en_programa.append(meses_es[current_month])
                
                # Avanzar al siguiente mes
                if current_month == 12:
                    current_month = 1
                    current_year += 1
                else:
                    current_month += 1
            
            # Formatear los meses según el ejemplo proporcionado
            if len(meses_en_programa) == 1:
                meses_formateados = meses_en_programa[0]
            else:
                meses_formateados = " - ".join(meses_en_programa)
            
            # Asignar el resultado al campo meses_en_el_programa
            registro_estado_2.meses_en_el_programa = meses_formateados
            
            # ⭐⭐ AGREGAR CAMPOS INDIVIDUALES PARA CADA MES ⭐⭐
            for mes in meses_objetivo:
                # Establecer 1 si el mes está en meses_en_programa, 0 si no
                valor = 1 if mes in meses_en_programa else 0
                setattr(registro_estado_2, mes, valor)
    
    return registros