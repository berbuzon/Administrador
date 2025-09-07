# services/report_service.py
import os
from sqlalchemy.orm import Session
import pandas as pd
import traceback

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
            # ⭐⭐ CONSULTA ORDENADA SEGÚN TUS CRITERIOS ⭐⭐
            datos_crudos = db.query(VistaOferta).order_by(
                VistaOferta.id_adolescente,
                VistaOferta.formulario_id, 
                VistaOferta.created_at,
                VistaOferta.updated_at
            ).all()
            
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
            # ⭐⭐ SOLUCIÓN PARA PERMISOS: Usar ruta absoluta en Documents ⭐⭐
            documents_path = os.path.expanduser("~/Documents")
            full_path = os.path.join(documents_path, filename)
            
            print("📊 Obteniendo datos de VistaOferta...")
            datos_crudos = ReportService.get_vista_oferta_cruda(db)
            print(f"✅ Obtenidos {len(datos_crudos)} registros crudos")
            
            print("📊 Obteniendo datos reconstruidos...")
            datos_reconstruidos = ReportService.get_vista_oferta_reconstruida(db)
            print(f"✅ Obtenidos {len(datos_reconstruidos)} registros reconstruidos")
            
            print("💾 Exportando a Excel...")
            with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
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
                        'updated_at': r.updated_at,
                        # ⭐⭐ NUEVO CAMPO: registro_agregado ⭐⭐
                    'registro_agregado': r.registro_agregado if hasattr(r, 'registro_agregado') else ''
                    } for r in datos_reconstruidos])
                    df_reconstruido.to_excel(writer, sheet_name='Vista_oferta_reconstruida', index=False)
                    print(f"✅ Hoja 'Vista_oferta_reconstruida' exportada: {len(df_reconstruido)} registros")
            
            print(f"✅ Reporte completo exportado: {full_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error exportando reporte: {e}")
            return False

    @staticmethod
    def analizar_secuencias(datos_reconstruidos: list[VistaOfertaReconstruida], filename: str = "analisis_secuencias.xlsx"):
        """
        Analiza las secuencias de estados y asignaciones por formulario
        directamente desde los objetos VistaOfertaReconstruida
        """
        try:
            # ⭐⭐ SOLUCIÓN PARA PERMISOS: Usar ruta absoluta en Documents ⭐⭐
            documents_path = os.path.expanduser("~/Documents")
            full_path = os.path.join(documents_path, filename)
            
            print("🔍 Analizando secuencias de estados y asignaciones...")
            
            # Convertir los objetos a DataFrame
            data = []
            for registro in datos_reconstruidos:
                data.append({
                    'formulario_id': registro.formulario_id,
                    'updated_at': registro.updated_at,
                    'asignada': 1 if registro.asignada else 0,
                    'estado': registro.estado
                })
            
            df = pd.DataFrame(data)
            
            # Ordenar por formulario y fecha
            df['updated_at'] = pd.to_datetime(df['updated_at'], errors="coerce")
            df = df.sort_values(['formulario_id', 'updated_at']).reset_index(drop=True)
            
            # Paso por formulario
            df['paso'] = df.groupby('formulario_id').cumcount() + 1
            detalle = df[['formulario_id', 'paso', 'updated_at', 'asignada', 'estado']].copy()  # ⭐⭐ .copy() evita el warning
            
            # ⭐⭐ SOLUCIÓN PARA ADVERTENCIA PANDAS: usar .loc ⭐⭐
            detalle.loc[:, 'par'] = detalle.apply(lambda r: f"({r['asignada']},{r['estado']})", axis=1)
            
            # Resumen por formulario
            resumen = (detalle.groupby('formulario_id')['par']
                    .apply(lambda s: " -> ".join(s.tolist()))
                    .reset_index(name='secuencia_(asignada,estado)'))
            
            # Frecuencia de secuencias
            frecuencia = (resumen.groupby('secuencia_(asignada,estado)')
                        .size()
                        .reset_index(name='frecuencia')
                        .sort_values('frecuencia', ascending=False)
                        .reset_index(drop=True))
            
            # Validar totales
            print("📊 Cantidad de formularios:", len(resumen))
            print("📊 Suma de frecuencias:", frecuencia['frecuencia'].sum())
            
            # Exportar a Excel
            with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
                detalle.to_excel(writer, index=False, sheet_name='detalle_secuencia')
                resumen.to_excel(writer, index=False, sheet_name='resumen_por_formulario')
                frecuencia.to_excel(writer, index=False, sheet_name='frecuencia_secuencias')
            
            print(f"✅ Análisis de secuencias exportado: {full_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error en análisis de secuencias: {e}")
            traceback.print_exc()
            return False