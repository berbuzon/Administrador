# services/calcula_cantidad_adolescentes_confirmados.py
from datetime import datetime
from typing import List, Dict, Set
import pandas as pd
from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida

def calcular_cantidad_confirmados_por_mes(registros: List[VistaOfertaReconstruida]) -> Dict[str, int]:
    """
    Calcula la cantidad única de adolescentes confirmados (estado=2) por mes
    utilizando los campos de meses ya calculados en VistaOfertaReconstruida.
    """
    # Diccionario para almacenar conjuntos de adolescentes por mes
    adolescentes_por_mes = {
        "enero": set(),
        "febrero": set(),
        "marzo": set(),
        "abril": set(),
        "mayo": set(),
        "junio": set(),
        "julio": set(),
        "agosto": set(),
        "septiembre": set(),
        "octubre": set(),
        "noviembre": set(),
        "diciembre": set()
    }
    
    # Procesar cada registro
    for registro in registros:
        # Solo considerar registros con estado=2 (confirmados)
        if registro.estado == 2:
            # Verificar cada mes
            meses = [
                ("enero", registro.enero),
                ("febrero", registro.febrero),
                ("marzo", registro.marzo),
                ("abril", registro.abril),
                ("mayo", registro.mayo),
                ("junio", registro.junio),
                ("julio", registro.julio),
                ("agosto", registro.agosto),
                ("septiembre", registro.septiembre),
                ("octubre", registro.octubre),
                ("noviembre", registro.noviembre),
                ("diciembre", registro.diciembre)
            ]
            
            for mes_name, valor in meses:
                if valor == 1:
                    adolescentes_por_mes[mes_name].add(registro.id_adolescente)
    
    # Convertir conjuntos a conteos
    conteo_por_mes = {mes: len(adolescentes) for mes, adolescentes in adolescentes_por_mes.items()}
    
    return conteo_por_mes

def calcular_altas_por_mes(registros: List[VistaOfertaReconstruida]) -> Dict[str, int]:
    """
    Calcula la cantidad de altas (nuevos estado=2) por mes, considerando solo adolescentes
    que no estaban confirmados en el mes anterior.
    """
    # Meses en español en orden
    meses_ordenados = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    # Primero, obtenemos el conjunto de adolescentes confirmados por mes (usando la lógica original)
    confirmados_por_mes = {}
    for mes in meses_ordenados:
        confirmados_por_mes[mes] = set()
    
    for registro in registros:
        if registro.estado == 2:
            for mes in meses_ordenados:
                if getattr(registro, mes, 0) == 1:
                    confirmados_por_mes[mes].add(registro.id_adolescente)
    
    # Ahora calculamos las altas: para cada mes, los adolescentes que están confirmados en ese mes
    # pero no en el mes anterior (si existe mes anterior)
    altas_por_mes = {}
    
    for i, mes in enumerate(meses_ordenados):
        if i == 0:
            # Para el primer mes, todas las confirmaciones son altas
            altas_por_mes[mes] = confirmados_por_mes[mes]
        else:
            mes_anterior = meses_ordenados[i-1]
            # Altas: adolescentes en el mes actual que no estaban en el mes anterior
            altas_por_mes[mes] = confirmados_por_mes[mes] - confirmados_por_mes[mes_anterior]
    
    return {mes: len(adolescentes) for mes, adolescentes in altas_por_mes.items()}

def calcular_bajas_por_mes(registros: List[VistaOfertaReconstruida]) -> Dict[str, int]:
    """
    Calcula la cantidad de bajas (estado=5) por mes, considerando adolescentes
    que estaban confirmados en el mes anterior pero no en el mes actual.
    """
    # Meses en español en orden
    meses_ordenados = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    # Obtenemos el conjunto de adolescentes confirmados por mes (usando la lógica original)
    confirmados_por_mes = {}
    for mes in meses_ordenados:
        confirmados_por_mes[mes] = set()
    
    for registro in registros:
        if registro.estado == 2:
            for mes in meses_ordenados:
                if getattr(registro, mes, 0) == 1:
                    confirmados_por_mes[mes].add(registro.id_adolescente)
    
    # Calculamos las bajas: para cada mes, los adolescentes que estaban confirmados en el mes anterior
    # pero no en el mes actual (excepto para el primer mes, que no hay bajas)
    bajas_por_mes = {}
    
    for i, mes in enumerate(meses_ordenados):
        if i == 0:
            # No hay mes anterior, por lo tanto no hay bajas
            bajas_por_mes[mes] = set()
        else:
            mes_anterior = meses_ordenados[i-1]
            # Bajas: adolescentes que estaban en el mes anterior pero no en el actual
            bajas_por_mes[mes] = confirmados_por_mes[mes_anterior] - confirmados_por_mes[mes]
    
    return {mes: len(adolescentes) for mes, adolescentes in bajas_por_mes.items()}

def generar_reporte_cantidad_confirmados(conteo_por_mes: Dict[str, int], 
                                        altas_por_mes: Dict[str, int],
                                        bajas_por_mes: Dict[str, int],
                                        output_path: str = "cantidad_confirmados_por_mes.xlsx"):
    """
    Genera un reporte Excel con la cantidad de adolescentes confirmados por mes,
    incluyendo altas y bajas. Excluye enero, febrero, marzo y meses posteriores al actual.
    """
    # Obtener mes actual
    mes_actual_num = datetime.now().month
    meses_ordenados = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    # Crear DataFrame con los resultados, excluyendo meses no deseados
    data = []
    for i, mes in enumerate(meses_ordenados):
        # Obtener número del mes (1-12)
        num_mes = i + 1
        
        # Excluir enero, febrero, marzo y meses posteriores al actual
        if num_mes < 4 or num_mes > mes_actual_num:
            continue
            
        data.append({
            "Mes": mes,
            "Confirmados": conteo_por_mes.get(mes, 0),
            "Altas": altas_por_mes.get(mes, 0),
            "Bajas": bajas_por_mes.get(mes, 0)
        })
    
    df = pd.DataFrame(data)
    
    # Ordenar por mes (cronológicamente)
    orden_meses = ["abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    # Verificar si hay datos
    if not df.empty:
        # Filtrar solo los meses que existen en el DataFrame
        orden_meses_existentes = [mes for mes in orden_meses if mes in df["Mes"].values]
        df["Orden"] = df["Mes"].apply(lambda x: orden_meses_existentes.index(x) if x in orden_meses_existentes else 99)
        df = df.sort_values("Orden").drop("Orden", axis=1)
    else:
        print("⚠️ No hay datos para generar el reporte de confirmados por mes")
    
    # Guardar en Excel
    df.to_excel(output_path, index=False)
    print(f"✅ Reporte de cantidad de confirmados por mes exportado: {output_path}")
    
    return df