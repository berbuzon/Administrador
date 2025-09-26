# services/report_service.py
import os
from sqlalchemy.orm import Session
import pandas as pd
import traceback
from datetime import datetime

# Importa ambos modelos
from models.reports.vista_oferta import VistaOferta
from models.reports.vista_oferta_reconstruida import VistaOfertaReconstruida, convertir_vistas_reconstruidas
from .calcula_cantidad_adolescentes_confirmados import calcular_cantidad_confirmados_por_mes, generar_reporte_cantidad_confirmados, calcular_altas_por_mes, calcular_bajas_por_mes

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
        Exporta TODOS los datos a Excel con múltiples hojas:
        - Vista_oferta: datos crudos
        - Vista_oferta_reconstruida: datos reconstruidos
        - Hojas mensuales: adolescentes confirmados (estado=2) por mes
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
                        'registro_agregado': r.registro_agregado if hasattr(r, 'registro_agregado') else '',
                        # ⭐⭐ NUEVO CAMPO: meses_en_el_programa ⭐⭐
                        'meses_en_el_programa': r.meses_en_el_programa if r.meses_en_el_programa else '',
                        # ⭐⭐ NUEVOS CAMPOS: meses individuales - TODOS LOS MESES ⭐⭐
                        'enero': getattr(r, 'enero', 0),
                        'febrero': getattr(r, 'febrero', 0),
                        'marzo': getattr(r, 'marzo', 0),  # ⭐⭐ COLUMNA MARZO AGREGADA ⭐⭐
                        'abril': getattr(r, 'abril', 0),
                        'mayo': getattr(r, 'mayo', 0),
                        'junio': getattr(r, 'junio', 0),
                        'julio': getattr(r, 'julio', 0),
                        'agosto': getattr(r, 'agosto', 0),
                        'septiembre': getattr(r, 'septiembre', 0),
                        'octubre': getattr(r, 'octubre', 0),
                        'noviembre': getattr(r, 'noviembre', 0),
                        'diciembre': getattr(r, 'diciembre', 0)
                    } for r in datos_reconstruidos])
                    df_reconstruido.to_excel(writer, sheet_name='Vista_oferta_reconstruida', index=False)
                    print(f"✅ Hoja 'Vista_oferta_reconstruida' exportada: {len(df_reconstruido)} registros")
                
                # ⭐⭐ NUEVO: Hojas mensuales con adolescentes confirmados (estado=2) ⭐⭐
                meses = [
                    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
                ]
                
                for mes in meses:
                    # Filtrar registros con estado=2 y presencia en el mes específico
                    registros_mes = [
                        r for r in datos_reconstruidos
                        if r.estado == 2 and getattr(r, mes, 0) == 1
                    ]

                    registros_mes_por_adolescente: dict[int, VistaOfertaReconstruida] = {}
                    for registro in registros_mes:
                        registro_existente = registros_mes_por_adolescente.get(registro.id_adolescente)
                        updated_at_registro = (
                            registro.updated_at if getattr(registro, "updated_at", None) else datetime.min
                        )
                        updated_at_existente = (
                            registro_existente.updated_at if getattr(registro_existente, "updated_at", None) else datetime.min
                        ) if registro_existente else datetime.min

                        if registro_existente is None or updated_at_registro > updated_at_existente:
                            registros_mes_por_adolescente[registro.id_adolescente] = registro

                    registros_mes_unicos = list(registros_mes_por_adolescente.values())

                    ids_unicos = {registro.id_adolescente for registro in registros_mes_unicos}
                    if len(ids_unicos) != len(registros_mes_unicos):
                        raise AssertionError(
                            f"Se encontraron IDs de adolescentes duplicados en la hoja del mes {mes}"
                        )

                    if registros_mes_unicos:
                        df_mes = pd.DataFrame([{
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
                            'asignada': 1 if r.asignada else 0,
                            'estado': r.estado,
                            'confirmado': 1 if r.confirmado else 0,
                            'created_at': r.created_at,
                            'updated_at': r.updated_at,
                            'registro_agregado': r.registro_agregado if hasattr(r, 'registro_agregado') else ''
                        } for r in registros_mes_unicos])
                        
                        # Limitar el nombre de la hoja a 31 caracteres (límite de Excel)
                        sheet_name = f"Confirmados_{mes}"[:31]
                        df_mes.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"✅ Hoja '{sheet_name}' exportada: {len(df_mes)} registros")
                    else:
                        print(f"⚠️ No hay registros confirmados para el mes de {mes}")
                
                print(f"✅ Reporte completo exportado: {full_path}")
                return True
                
        except Exception as e:
            print(f"❌ Error exportando reporte: {e}")
            traceback.print_exc()
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

    @staticmethod
    def generar_reporte_confirmados_por_mes(db: Session, filename: str = "cantidad_confirmados_por_mes.xlsx"):
        """
        Genera un reporte con la cantidad de adolescentes confirmados por mes,
        incluyendo altas y bajas
        """
        try:
            print("📊 Obteniendo datos reconstruidos para reporte de confirmados por mes...")
            datos_reconstruidos = ReportService.get_vista_oferta_reconstruida(db)
            
            print("🧮 Calculando cantidad de confirmados por mes...")
            conteo_por_mes = calcular_cantidad_confirmados_por_mes(datos_reconstruidos)
            
            print("📈 Calculando altas por mes...")
            altas_por_mes = calcular_altas_por_mes(datos_reconstruidos)
            
            print("📉 Calculando bajas por mes...")
            bajas_por_mes = calcular_bajas_por_mes(datos_reconstruidos)
            
            print("💾 Exportando reporte de confirmados por mes...")
            # ⭐⭐ SOLUCIÓN PARA PERMISOS: Usar ruta absoluta en Documents ⭐⭐
            documents_path = os.path.expanduser("~/Documents")
            full_path = os.path.join(documents_path, filename)
            
            df = generar_reporte_cantidad_confirmados(conteo_por_mes, altas_por_mes, bajas_por_mes, full_path)
            
            print(f"✅ Reporte de confirmados por mes exportado: {full_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error generando reporte de confirmados por mes: {e}")
            traceback.print_exc()
            return False
        

    # services/report_service.py (actualizar el método)
    @staticmethod
    def generar_reporte_presupuesto_becas(db: Session, filename: str = "presupuesto_becas.xlsx"):
        """
        Genera un reporte con el análisis presupuestario de becas
        """
        try:
            print("📊 Obteniendo datos reconstruidos para análisis de presupuesto...")
            datos_reconstruidos = ReportService.get_vista_oferta_reconstruida(db)
            
            print("🧮 Calculando métricas para presupuesto...")
            from .calcula_cantidad_adolescentes_confirmados import calcular_cantidad_confirmados_por_mes, calcular_altas_por_mes, calcular_bajas_por_mes
            conteo_por_mes = calcular_cantidad_confirmados_por_mes(datos_reconstruidos)
            altas_por_mes = calcular_altas_por_mes(datos_reconstruidos)
            bajas_por_mes = calcular_bajas_por_mes(datos_reconstruidos)
            
            print("💰 Calculando presupuesto de becas...")
            from .calcula_presupuesto_becas import generar_reporte_presupuesto
            
            # ⭐⭐ SOLUCIÓN PARA PERMISOS: Usar ruta absoluta en Documents ⭐⭐
            documents_path = os.path.expanduser("~/Documents")
            full_path = os.path.join(documents_path, filename)
            
            df = generar_reporte_presupuesto(conteo_por_mes, altas_por_mes, bajas_por_mes, full_path)
            
            print(f"✅ Reporte de presupuesto de becas exportado: {full_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error generando reporte de presupuesto: {e}")
            traceback.print_exc()
            return False