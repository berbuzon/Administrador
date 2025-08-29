# services/report_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, and_
from datetime import datetime
import pandas as pd

# Importa correctamente el modelo
from src.database.models_manual import VistaOferta

class ReportService:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_adolescentes_aceptados_por_mes_vista(db: Session, fecha_inicio: str = '2025-03-17'):
        """
        Obtiene adolescentes aceptados por mes usando la vista vista_oferta
        """
        try:
            query = db.query(
                func.year(VistaOferta.updated_at).label('ano'),
                func.month(VistaOferta.updated_at).label('mes'),
                func.count(distinct(VistaOferta.id_adolescente)).label('total_adolescentes')
            ).filter(
                VistaOferta.confirmado == True,
                VistaOferta.asignada == True,
                VistaOferta.estado == 2,
                VistaOferta.updated_at >= fecha_inicio
            ).group_by(
                func.year(VistaOferta.updated_at),
                func.month(VistaOferta.updated_at)
            ).order_by(
                'ano', 'mes'
            )
            
            return query.all()
            
        except Exception as e:
            print(f"❌ Error en la consulta con vista: {e}")
            raise
    
    @staticmethod
    def get_detalle_completo_vista(db: Session, filters: dict = None):
        """
        Obtiene el detalle completo desde la vista con filtros opcionales
        """
        try:
            query = db.query(VistaOferta)
            
            # Aplicar filtros si se proporcionan
            if filters:
                if filters.get('confirmado') is not None:
                    query = query.filter(VistaOferta.confirmado == filters['confirmado'])
                if filters.get('asignada') is not None:
                    query = query.filter(VistaOferta.asignada == filters['asignada'])
                if filters.get('estado') is not None:
                    query = query.filter(VistaOferta.estado == filters['estado'])
                if filters.get('fecha_desde'):
                    query = query.filter(VistaOferta.updated_at >= filters['fecha_desde'])
            
            return query.order_by(VistaOferta.id_adolescente, VistaOferta.updated_at).all()
            
        except Exception as e:
            print(f"❌ Error obteniendo detalle desde vista: {e}")
            return []
    
    @staticmethod
    def get_estadisticas_vista(db: Session):
        """
        Obtiene estadísticas generales desde la vista
        """
        try:
            # Total de registros
            total = db.query(func.count(VistaOferta.id)).scalar()
            
            # Por estado
            por_estado = db.query(
                VistaOferta.estado,
                func.count(VistaOferta.id).label('cantidad')
            ).group_by(VistaOferta.estado).all()
            
            # Por asignación
            por_asignacion = db.query(
                VistaOferta.asignada,
                func.count(VistaOferta.id).label('cantidad')
            ).group_by(VistaOferta.asignada).all()
            
            # Por confirmación
            por_confirmacion = db.query(
                VistaOferta.confirmado,
                func.count(VistaOferta.id).label('cantidad')
            ).group_by(VistaOferta.confirmado).all()
            
            return {
                'total_registros': total,
                'por_estado': por_estado,
                'por_asignacion': por_asignacion,
                'por_confirmacion': por_confirmacion
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    @staticmethod
    def get_adolescentes_aceptados_dataframe_vista(db: Session, fecha_inicio: str = '2025-03-17'):
        """
        Devuelve los datos de la vista como DataFrame de pandas
        """
        try:
            data = ReportService.get_adolescentes_aceptados_por_mes_vista(db, fecha_inicio)
            
            if not data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data, columns=['año', 'mes', 'total_adolescentes'])
            df['mes_nombre'] = df['mes'].apply(lambda x: datetime(2023, x, 1).strftime('%B'))
            df['periodo'] = df['año'].astype(str) + '-' + df['mes'].astype(str).str.zfill(2)
            df = df.sort_values(['año', 'mes'])
            
            return df
            
        except Exception as e:
            print(f"❌ Error creando DataFrame desde vista: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def exportar_detalle_completo(db: Session, filename: str = None):
        """
        Exporta todo el detalle de la vista a Excel
        """
        try:
            # Obtener todos los datos de la vista con los filtros deseados
            datos = db.query(VistaOferta).filter(
                VistaOferta.confirmado == True,
                VistaOferta.asignada == True,
                VistaOferta.estado == 2
            ).all()
            
            if not datos:
                print("⚠️ No se encontraron datos para exportar")
                return False
            
            # Crear DataFrame
            data_list = []
            for registro in datos:
                data_list.append({
                    'id_adolescente': registro.id_adolescente,
                    'nombre': registro.nombre,
                    'apellido': registro.apellido,
                    'dni': registro.dni,
                    'sede': registro.sede,
                    'actividad': registro.actividad,
                    'dia': registro.dia,
                    'horario': registro.horario,
                    'asignada': 'Asignada' if registro.asignada else 'No asignada',
                    'estado': ReportService.get_estado_texto(registro.estado),
                    'confirmado': 'Confirmado' if registro.confirmado else 'No confirmado',
                    'updated_at': registro.updated_at
                })
            
            df = pd.DataFrame(data_list)
            
            # Crear nombre de archivo con timestamp
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"detalle_completo_vista_{timestamp}.xlsx"
            
            # Guardar en Excel
            df.to_excel(filename, index=False, sheet_name='Detalle Completo')
            
            print(f"✓ Exportado {len(df)} registros a '{filename}'")
            return True
            
        except Exception as e:
            print(f"❌ Error exportando detalle: {e}")
            return False

    @staticmethod
    def get_estado_texto(estado: int) -> str:
        """Convierte el código de estado a texto"""
        estados = {
            0: 'Sin datos',
            1: 'Pendiente', 
            2: 'Aceptado',
            3: 'Sin datos',
            4: 'Cambio de actividad',
            5: 'Baja de actividad'
        }
        return estados.get(estado, 'Desconocido')