import os
from datetime import datetime
from typing import Dict, List

import pandas as pd
from sqlalchemy.orm import Session


CAMPOS_MESES: List[str] = [
    'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]


def _to_bit(value) -> int:
    """Normaliza el valor de un campo de mes a 0 o 1."""
    if isinstance(value, bool):
        return int(value)

    if value is None:
        return 0

    if isinstance(value, (int, float)):
        return 1 if value != 0 else 0

    if isinstance(value, str):
        value_normalizado = value.strip().lower()
        if value_normalizado in {'', '0', 'no', 'false', 'f', 'n'}:
            return 0
        return 1

    return 1 if value else 0


def consolidar_por_adolescente(registros_estado_dos) -> List[Dict[str, object]]:
    """Agrupa registros por adolescente consolidando meses asistidos y datos recientes."""

    def _obtener_fecha(registro):
        fecha = getattr(registro, 'updated_at', None)
        return fecha if isinstance(fecha, datetime) else datetime.min

    agrupados: Dict[int, Dict[str, object]] = {}

    for registro in registros_estado_dos:
        id_adolescente = getattr(registro, 'id_adolescente', None)
        if id_adolescente is None:
            continue

        fecha_registro = _obtener_fecha(registro)
        entrada = agrupados.get(id_adolescente)

        if entrada is None:
            agrupados[id_adolescente] = {
                'registro_reciente': registro,
                'fecha_reciente': fecha_registro,
                'meses': {mes: _to_bit(getattr(registro, mes, 0)) for mes in CAMPOS_MESES},
            }
            continue

        for mes in CAMPOS_MESES:
            valor_actual = _to_bit(getattr(registro, mes, 0))
            if valor_actual:
                entrada['meses'][mes] = 1

        if fecha_registro >= entrada['fecha_reciente']:
            entrada['registro_reciente'] = registro
            entrada['fecha_reciente'] = fecha_registro

    filas = []
    for id_adolescente, data in sorted(agrupados.items()):
        registro_reciente = data['registro_reciente']
        meses_asistidos = [mes for mes, valor in data['meses'].items() if valor == 1]

        filas.append({
            'id_adolescente': id_adolescente,
            'Nombre': getattr(registro_reciente, 'Nombre', ''),
            'Apellido': getattr(registro_reciente, 'Apellido', ''),
            'DNI': getattr(registro_reciente, 'DNI', ''),
            'Sede': getattr(registro_reciente, 'Sede', ''),
            'Actividad': getattr(registro_reciente, 'Actividad', ''),
            'cantidad_meses_sin_marzo': len(meses_asistidos),
            'meses_asistidos_sin_marzo': ' - '.join(meses_asistidos) if meses_asistidos else '',
        })

    return filas


def _get_report_service():
    from .report_service import ReportService

    return ReportService


def generar_reporte_meses(db: Session, filename: str = "reporte_meses.xlsx") -> str:
    """Genera un reporte en Excel con la cantidad de meses asistidos por adolescente excluyendo marzo."""
    report_service = _get_report_service()
    registros = report_service.get_vista_oferta_reconstruida(db)
    registros_estado_dos = [r for r in registros if getattr(r, 'estado', None) == 2]

    detalle_rows = consolidar_por_adolescente(registros_estado_dos)

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
