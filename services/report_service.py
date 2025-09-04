# services/report_service.py (ARCHIVO COMPLETO ACTUALIZADO)
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import datetime
import pandas as pd

# Importa ambos modelos
from models.reports.vista_oferta import VistaOferta
from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida, convertir_vistas_reconstruidas

class ReportService:
    
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
        (Versión original - devuelve VistaOferta)
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
    def get_detalle_completo_vista_reconstruido(db: Session, filters: dict = None) -> list[VistaOfertaReconstruida]:
        """
        Obtiene el detalle completo desde la vista y lo convierte a VistaOfertaReconstruida
        (NUEVA VERSIÓN - devuelve objetos reconstruidos)
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
            
            resultados = query.order_by(VistaOferta.id_adolescente, VistaOferta.updated_at).all()
            
            # Convertir a objetos reconstruidos
            return convertir_vistas_reconstruidas(resultados)
            
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
    
    # services/report_service.py (método adicional para archivo único con múltiples hojas)
    @staticmethod
    def exportar_todo_en_un_archivo(db: Session, filename: str = "reporte_completo_adolescentes.xlsx"):
        """
        Exporta todos los datos a un solo archivo Excel con múltiples hojas
        """
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Hoja 1: Resumen mensual
                df_resumen = ReportService.get_adolescentes_aceptados_dataframe_vista(db)
                if not df_resumen.empty:
                    df_resumen.to_excel(writer, sheet_name='Resumen Mensual', index=False)
                
                # Hoja 2: Detalle reconstruido
                datos_reconstruidos = ReportService.get_detalle_completo_vista_reconstruido(db, {
                    'confirmado': True,
                    'asignada': True,
                    'estado': 2
                })
                if datos_reconstruidos:
                    df_detalle = pd.DataFrame([dato.to_dict() for dato in datos_reconstruidos])
                    df_detalle.to_excel(writer, sheet_name='Detalle Completo', index=False)
            
            print(f"✅ Reporte completo exportado: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exportando reporte completo: {e}")
            return False