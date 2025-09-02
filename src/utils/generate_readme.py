import os
import re
from datetime import datetime

def generate_readme_from_structure():
    """
    Genera/actualiza README.md manteniendo secciones personalizadas
    y actualizando solo la estructura del proyecto
    """
    try:
        # Leer la estructura desde estructura.txt
        with open('estructura.txt', 'r', encoding='utf-8') as f:
            structure_content = f.read().strip()
        
        # Leer README.md existente si existe
        existing_readme = ""
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                existing_readme = f.read()
        
        # Plantilla base si no existe README
        if not existing_readme:
            readme_content = create_complete_readme(structure_content)
        else:
            # Actualizar solo la sección de estructura
            readme_content = update_existing_readme(existing_readme, structure_content)
        
        # Escribir el README.md
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README.md actualizado correctamente")
        print("📍 Se mantuvieron secciones personalizadas")
        
    except FileNotFoundError:
        print("❌ Error: No se encontró estructura.txt")
        print("💡 Ejecuta primero: python src/utils/update_structure.py")

def create_complete_readme(structure_content):
    """Crear README completo desde cero"""
    return f"""# 🐍 Administrador - Sistema de Gestión

Sistema administrativo para gestión de base de datos con Python.

## 📁 Estructura del Proyecto

```plaintext
{structure_content}
"""