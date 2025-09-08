# services/calcula_presupuesto_becas.py
from datetime import datetime
from typing import Dict
import pandas as pd

def calcular_presupuesto_becas(conteo_por_mes: Dict[str, int], altas_por_mes: Dict[str, int], bajas_por_mes: Dict[str, int]) -> pd.DataFrame:
    """
    Calcula el presupuesto de becas mes a mes, incluyendo altas y bajas
    """
    # Montos de beca por mes
    montos_beca = {
        "abril": 15000,
        "mayo": 15000,
        "junio": 15000,
        "julio": 16200,
        "agosto": 16200,
        "septiembre": 16200,
        "octubre": 16200,
        "noviembre": 16200,
        "diciembre": 16200
    }
    
    # Obtener mes actual
    mes_actual_num = datetime.now().month
    meses_ordenados = ["abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    # Filtrar meses hasta el actual
    meses_a_considerar = []
    for i, mes in enumerate(meses_ordenados):
        if i + 4 <= mes_actual_num:  # Abril es el mes 4
            meses_a_considerar.append(mes)
    
    # Agregar meses de octubre, noviembre y diciembre
    meses_proyeccion = ["octubre", "noviembre", "diciembre"]
    for mes in meses_proyeccion:
        if mes not in meses_a_considerar:
            meses_a_considerar.append(mes)
    
    # Calcular datos presupuestarios
    data = []
    excedente_acumulado = 0
    
    for mes in meses_a_considerar:
        # Para meses de octubre, noviembre y diciembre siempre usar 7231 adolescentes
        if mes in meses_proyeccion:
            adolescentes_reales = 7231
            altas_mes = 0
            bajas_mes = 0
        else:
            adolescentes_reales = conteo_por_mes.get(mes, 0)
            altas_mes = altas_por_mes.get(mes, 0)
            bajas_mes = bajas_por_mes.get(mes, 0)
        
        monto_por_adolescente = montos_beca[mes]
        
        # Gasto real
        gasto_real = adolescentes_reales * monto_por_adolescente
        
        # Gasto planeado (presupuesto base: 7,000 adolescentes)
        gasto_planeado = 7000 * monto_por_adolescente
        
        # Excedente del mes
        excedente_mes = gasto_planeado - gasto_real
        excedente_acumulado += excedente_mes
        
        data.append({
            "Mes": mes,
            "Adolescentes confirmados": adolescentes_reales,
            "Altas (nuevos estado=2)": altas_mes,
            "Bajas (estado=5)": bajas_mes,
            "Monto por adolescente": monto_por_adolescente,
            "Gasto real": gasto_real,
            "Gasto planeado": gasto_planeado,
            "Excedente del mes": excedente_mes,
            "Excedente acumulado": excedente_acumulado
        })
    
    return pd.DataFrame(data)

def generar_reporte_presupuesto(conteo_por_mes: Dict[str, int], altas_por_mes: Dict[str, int], bajas_por_mes: Dict[str, int], output_path: str = "presupuesto_becas.xlsx"):
    """
    Genera un reporte Excel con el análisis presupuestario de becas, incluyendo altas y bajas
    """
    df = calcular_presupuesto_becas(conteo_por_mes, altas_por_mes, bajas_por_mes)
    
    if df.empty:
        print("⚠️ No hay datos para generar el reporte de presupuesto")
        return df
    
    # Formatear números con separadores de miles (usando PUNTOS en lugar de comas)
    df_formateado = df.copy()
    columnas_numericas = ['Adolescentes confirmados', 'Altas (nuevos estado=2)', 'Bajas (estado=5)', 
                         'Monto por adolescente', 'Gasto real', 'Gasto planeado', 
                         'Excedente del mes', 'Excedente acumulado']
    
    for col in columnas_numericas:
        df_formateado[col] = df_formateado[col].apply(lambda x: f"{x:,.0f}".replace(",", ".") if pd.notnull(x) else "")
    
    # Guardar en Excel
    df_formateado.to_excel(output_path, index=False, sheet_name='Presupuesto')
    
    print(f"✅ Reporte de presupuesto exportado: {output_path}")
    return df