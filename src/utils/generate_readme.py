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
        
    except FileNotFoundError:
        print("❌ Error: No se encontró estructura.txt")
        print("💡 Ejecuta primero: python src/utils/update_structure.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def create_complete_readme(structure_content):
    """Crear README completo desde cero"""
    content = [
        "# 🐍 Administrador - Sistema de Gestión",
        "",
        "Sistema administrativo para gestión de base de datos con Python.",
        "",
        "## 📁 Estructura del Proyecto",
        "",
        "```plaintext",
        structure_content,
        "```",
        "",
        "## 🚀 Instalación",
        "",
        "```bash",
        "git clone https://github.com/berbuzon/Administrador.git",
        "cd Administrador",
        "pip install -r requirements.txt",
        "```",
        "",
        "## 🎯 Uso",
        "",
        "```bash",
        "python main.py",
        "```",
        "",
        "## 🔧 Mantenimiento",
        "",
        "```bash",
        "# Actualizar documentación:",
        "python src/utils/update_docs.py",
        "```",
        "",
        "---",
        f"> 📅 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    return '\n'.join(content)

def update_existing_readme(existing_readme, structure_content):
    """Actualizar solo la sección de estructura en README existente"""
    try:
        # Patrón para encontrar la sección de estructura
        pattern = r'(## 📁 Estructura del Proyecto\n\n```plaintext\n).*?(\n```)'
        replacement = r'\1' + structure_content + r'\2'
        
        # Reemplazar solo la sección de estructura
        if re.search(pattern, existing_readme, re.DOTALL):
            updated_readme = re.sub(pattern, replacement, existing_readme, flags=re.DOTALL)
        else:
            # Si no existe la sección, agregarla después del título
            updated_readme = existing_readme.replace(
                '# 🐍 Administrador - Sistema de Gestión\n',
                '# 🐍 Administrador - Sistema de Gestión\n\n## 📁 Estructura del Proyecto\n\n```plaintext\n' + structure_content + '\n```\n'
            )
        
        # Agregar fecha de actualización
        if 'Última actualización:' not in updated_readme:
            updated_readme += '\n---\n> 📅 Última actualización: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            updated_readme = re.sub(
                r'Última actualización: .*',
                'Última actualización: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                updated_readme
            )
        
        return updated_readme
        
    except Exception as e:
        print(f"❌ Error en update_existing_readme: {e}")
        # Si hay error, crear uno nuevo
        return create_complete_readme(structure_content)

if __name__ == "__main__":
    generate_readme_from_structure()