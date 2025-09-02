import os
from pathlib import Path

def generate_structure_file():
    """
    Genera el archivo estructura.txt con la estructura actual del proyecto
    """
    base_dir = Path(".")
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv'}
    ignore_files = {'.DS_Store', 'estructura.txt', 'estructura_actual.txt'}
    
    structure_lines = ["Administrador/"]
    
    for item in sorted(base_dir.rglob("*")):
        # Ignorar carpetas no deseadas
        if any(part in ignore_dirs for part in item.parts):
            continue
        
        # Ignorar archivos no deseados
        if item.name in ignore_files:
            continue
        
        # Calcular profundidad e indentación
        depth = len(item.relative_to(base_dir).parts)
        indent = "│   " * (depth - 1) + "├── " if depth > 0 else ""
        
        if item.is_file():
            structure_lines.append(f"{indent}{item.name}")
        elif item.is_dir() and item != base_dir:
            structure_lines.append(f"{indent}{item.name}/")
    
    # Escribir archivo
    with open('estructura.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(structure_lines))
    
    print("✅ estructura.txt generado correctamente")

if __name__ == "__main__":
    generate_structure_file()