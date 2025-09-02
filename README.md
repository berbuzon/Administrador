# 🐍 Administrador - Sistema de Gestión

Sistema administrativo para gestión de base de datos con Python.

## 📁 Estructura del Proyecto

```plaintext
Administrador/
├── .env
├── .gitignore
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── database.py
│   ├── settings.py
├── debug_simple.py
├── main.py
├── main_funcional.py
├── models/
│   ├── __init__.py
│   ├── models.py
├── README.md
├── reporte_adolescentes_aceptados_20250829_083627.xlsx
├── reporte_adolescentes_aceptados_20250902_095609.xlsx
├── reporte_adolescentes_aceptados_20250902_121023.xlsx
├── requirements.txt
├── services/
│   ├── __init__.py
│   ├── report_service.py
├── src/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── conexiones.py
│   │   ├── models_manual.py
│   ├── demo/
│   │   ├── __init__.py
│   │   ├── demo_manual.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── model_utils.py
│   │   ├── query_utils.py
│   │   ├── storage_utils.py
│   │   ├── update_structure.py
├── test_config.py
├── test_consulta_directa.py
├── test_env.py
├── test_import.py
├── test_minimo.py
├── test_report_service.py
├── test_vista.py
```

## 🚀 Instalación

```bash
git clone https://github.com/berbuzon/Administrador.git
cd Administrador
pip install -r requirements.txt
```

## 🎯 Uso

```bash
python main.py
```

## 🔧 Mantenimiento

```bash
# Actualizar documentación:
python src/utils/update_docs.py
```

---
> 📅 Última actualización: 2025-09-02 13:45:53
