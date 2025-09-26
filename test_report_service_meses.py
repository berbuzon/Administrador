import os
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

import pandas as pd

from services.report_service_meses import generar_reporte_meses


class DummyRegistro:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class GenerarReporteMesesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_reporte_excluye_marzo_en_detalle_y_frecuencia(self):
        registros = [
            DummyRegistro(
                id_adolescente=1,
                Nombre='Ana',
                Apellido='García',
                DNI='123',
                Sede='Centro',
                Actividad='Arte',
                estado=2,
                updated_at=datetime(2024, 5, 1),
                enero=1,
                marzo=1,
                abril=1
            ),
            DummyRegistro(
                id_adolescente=1,
                Nombre='Ana',
                Apellido='García',
                DNI='123',
                Sede='Centro',
                Actividad='Arte',
                estado=2,
                updated_at=datetime(2024, 7, 1),
                febrero=1,
                marzo=1,
                noviembre=1
            ),
            DummyRegistro(
                id_adolescente=2,
                Nombre='Luis',
                Apellido='Pérez',
                DNI='456',
                Sede='Norte',
                Actividad='Deporte',
                estado=2,
                updated_at=datetime(2024, 3, 1),
                marzo=1
            ),
            DummyRegistro(
                id_adolescente=3,
                Nombre='Eva',
                Apellido='López',
                DNI='789',
                Sede='Sur',
                Actividad='Música',
                estado=1,
                updated_at=datetime(2024, 6, 1),
                abril=1
            )
        ]

        documents_dir = self.temp_dir.name

        class FakeReportService:
            @staticmethod
            def get_vista_oferta_reconstruida(_db):
                return registros

        original_expanduser = os.path.expanduser

        with patch('services.report_service_meses._get_report_service', return_value=FakeReportService), \
             patch('services.report_service_meses.os.path.expanduser',
                   side_effect=lambda path: documents_dir if path == '~/Documents' else original_expanduser(path)):
            output_path = generar_reporte_meses(None, filename='reporte_prueba.xlsx')

        self.assertTrue(os.path.exists(output_path))

        libro = pd.ExcelFile(output_path)
        detalle = pd.read_excel(libro, 'Meses_por_adolescente')
        frecuencia = pd.read_excel(libro, 'Frecuencia_por_meses')

        detalle_por_id = detalle.set_index('id_adolescente')

        self.assertEqual(detalle_por_id.loc[1, 'cantidad_meses_sin_marzo'], 2)
        self.assertEqual(detalle_por_id.loc[1, 'meses_asistidos_sin_marzo'], 'febrero - noviembre')
        self.assertEqual(detalle_por_id.loc[2, 'cantidad_meses_sin_marzo'], 0)
        valor_meses_id2 = detalle_por_id.loc[2, 'meses_asistidos_sin_marzo']
        self.assertTrue(pd.isna(valor_meses_id2) or valor_meses_id2 == '')

        self.assertNotIn('marzo', ''.join(detalle['meses_asistidos_sin_marzo'].dropna()))

        frecuencia_por_cantidad = frecuencia.set_index('cantidad_meses_sin_marzo')['frecuencia'].to_dict()
        self.assertEqual(frecuencia_por_cantidad.get(2), 1)
        self.assertEqual(frecuencia_por_cantidad.get(0), 1)
        self.assertEqual(len(frecuencia_por_cantidad), 2)


if __name__ == '__main__':
    unittest.main()
