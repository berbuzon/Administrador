# services/report_service.py
from sqlalchemy.orm import Session
import pandas as pd

# Importa ambos modelos
from models.reports.vista_oferta import VistaOferta
from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida, convertir_vistas_reconstruidas

class ReportService:
    
    @staticmethod
    def get_vista_oferta_cruda(db: Session) -> list[VistaOferta]:
        """
        Obtiene TODOS los datos crudos de VistaOferta sin filtros
        """
        try:
            return db.query(VistaOferta).order_by(VistaOferta.id_adolescente).all()
        except Exception as e:
            print(f"❌ Error obteniendo datos crudos: {e}")
            return []
    
    @staticmethod
    def get_vista_oferta_reconstruida(db: Session) -> list[VistaOfertaReconstruida]:
        """
        Obtiene TODOS los datos reconstruidos sin filtros
        """
        try:
            datos_crudos = db.query(VistaOferta).order_by(VistaOferta.id_adolescente).all()
            return convertir_vistas_reconstruidas(datos_crudos)
        except Exception as e:
            print(f"❌ Error obteniendo datos reconstruidos: {e}")
            return []
    
    @staticmethod
    def exportar_todo_a_excel(db: Session, filename: str = "reporte_completo.xlsx"):
        """
        Exporta TODOS los datos a Excel con dos hojas sin filtros
        Campos booleanos como 0 y 1
        """
        try:
            print("📊 Obteniendo datos de VistaOferta...")
            datos_crudos = ReportService.get_vista_oferta_cruda(db)
            print(f"✅ Obtenidos {len(datos_crudos)} registros crudos")
            
            print("📊 Obteniendo datos reconstruidos...")
            datos_reconstruidos = ReportService.get_vista_oferta_reconstruida(db)
            print(f"✅ Obtenidos {len(datos_reconstruidos)} registros reconstruidos")
            
            print("💾 Exportando a Excel...")
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Hoja 1: VistaOferta cruda (booleanos como 0 y 1)
                if datos_crudos:
                    df_crudo = pd.DataFrame([{
                        'id_adolescente': r.id_adolescente,
                        'Nombre': r.Nombre,
                        'Apellido': r.Apellido,
                        'DNI': r.DNI,
                        'Sede': r.Sede,
                        'Actividad': r.Actividad,
                        'Dia': r.Dia,
                        'Horario': r.Horario,
                        'formulario_id': r.formulario_id,
                        'oferta_actividad_id': r.oferta_actividad_id,
                        # ⭐⭐ BOOLEANOS COMO 0 Y 1 ⭐⭐
                        'asignada': 1 if r.asignada else 0,
                        'estado': r.estado,  # Este ya es entero
                        'confirmado': 1 if r.confirmado else 0,
                        'created_at': r.created_at,
                        'updated_at': r.updated_at
                    } for r in datos_crudos])
                    df_crudo.to_excel(writer, sheet_name='Vista_oferta', index=False)
                    print(f"✅ Hoja 'Vista_oferta' exportada: {len(df_crudo)} registros")
                
                # Hoja 2: VistaOferta reconstruida (booleanos como 0 y 1)
                if datos_reconstruidos:
                    df_reconstruido = pd.DataFrame([{
                        'id_adolescente': r.id_adolescente,
                        'Nombre': r.Nombre,
                        'Apellido': r.Apellido,
                        'DNI': r.DNI,
                        'Sede': r.Sede,
                        'Actividad': r.Actividad,
                        'Dia': r.Dia,
                        'Horario': r.Horario,
                        'formulario_id': r.formulario_id,
                        'oferta_actividad_id': r.oferta_actividad_id,
                        # ⭐⭐ BOOLEANOS COMO 0 Y 1 ⭐⭐
                        'asignada': 1 if r.asignada else 0,
                        'estado': r.estado,  # Este ya es entero
                        'confirmado': 1 if r.confirmado else 0,
                        'created_at': r.created_at,
                        'updated_at': r.updated_at
                    } for r in datos_reconstruidos])
                    df_reconstruido.to_excel(writer, sheet_name='Vista_oferta_reconstruida', index=False)
                    print(f"✅ Hoja 'Vista_oferta_reconstruida' exportada: {len(df_reconstruido)} registros")
            
            print(f"✅ Reporte completo exportado: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exportando reporte: {e}")
            return False