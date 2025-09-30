import os
from datetime import datetime
from typing import List

import pandas as pd
from sqlalchemy.orm import Session


MESES_SIN_MARZO: List[str] = [
    'enero', 'febrero', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]


def _obtener_registro_mas_reciente(registro_actual, registro_existente):
    """Devuelve el registro con el ``updated_at`` más reciente.

    Los datos de "oferta reconstruida" pueden traer múltiples filas por
    adolescente. En esos casos queremos conservar el registro más actual para
    reflejar los meses asistidos más cercanos a la fecha del informe. Si alguna
    de las fechas estuviera ausente, se considera como la menos reciente.
    """

    fecha_actual = getattr(registro_actual, 'updated_at', None) or datetime.min
    fecha_existente = getattr(registro_existente, 'updated_at', None) or datetime.min
    return registro_actual if fecha_actual >= fecha_existente else registro_existente


def _get_report_service():
    from .report_service import ReportService

    return ReportService


def generar_reporte_meses(db: Session, filename: str = "reporte_meses.xlsx") -> str:
    """Genera un reporte en Excel con la cantidad de meses asistidos por adolescente excluyendo marzo."""
    report_service = _get_report_service()
    registros = report_service.get_vista_oferta_reconstruida(db)
    registros_estado_dos = [r for r in registros if getattr(r, 'estado', None) == 2]

    registros_por_adolescente = {}
    for registro in registros_estado_dos:
        existente = registros_por_adolescente.get(registro.id_adolescente)
        if existente is None:
            registros_por_adolescente[registro.id_adolescente] = registro
        else:
            registros_por_adolescente[registro.id_adolescente] = _obtener_registro_mas_reciente(
                registro,
                existente
            )

    registros_unicos = sorted(
        registros_por_adolescente.values(),
        key=lambda r: getattr(r, 'id_adolescente', 0)
    )

    detalle_rows = []
    for registro in registros_unicos:
        meses_asistidos = [mes for mes in MESES_SIN_MARZO if getattr(registro, mes, 0) == 1]
        detalle_rows.append({
            'id_adolescente': getattr(registro, 'id_adolescente', None),
            'Nombre': getattr(registro, 'Nombre', ''),
            'Apellido': getattr(registro, 'Apellido', ''),
            'DNI': getattr(registro, 'DNI', ''),
            'Sede': getattr(registro, 'Sede', ''),
            'Actividad': getattr(registro, 'Actividad', ''),
            'cantidad_meses_sin_marzo': len(meses_asistidos),
            'meses_asistidos_sin_marzo': ' - '.join(meses_asistidos)
        })

    df_detalle = pd.DataFrame(detalle_rows)

    if not df_detalle.empty:
        frecuencia_series = df_detalle['cantidad_meses_sin_marzo'].value_counts().sort_index()
        df_frecuencia = frecuencia_series.reset_index()
        df_frecuencia.columns = ['cantidad_meses_sin_marzo', 'frecuencia']
    else:
        df_frecuencia = pd.DataFrame(columns=['cantidad_meses_sin_marzo', 'frecuencia'])

    documents_path = os.path.expanduser('~/Documents')
    os.makedirs(documents_path, exist_ok=True)
    full_path = os.path.join(documents_path, filename)

    with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
        df_detalle.to_excel(writer, sheet_name='Meses_por_adolescente', index=False)
        df_frecuencia.to_excel(writer, sheet_name='Frecuencia_por_meses', index=False)

    return full_path
