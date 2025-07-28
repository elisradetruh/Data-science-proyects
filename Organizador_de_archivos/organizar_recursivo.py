import os
import shutil
from pathlib import Path
from typing import Dict, List, Set

def definir_categorias() -> Dict[str, List[str]]:
    """Define las categorías de archivos y sus extensiones."""
    return {
        "Imagenes": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
        "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".doc", ".rtf", ".odt"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
        "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Programas": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
        "Otros": []
    }

def crear_diccionario_extensiones(categorias: Dict[str, List[str]]) -> Dict[str, str]:
    """Crea un diccionario que mapea extensiones a categorías."""
    extension_a_categoria = {}
    for categoria, extensiones in categorias.items():
        for ext in extensiones:
            extension_a_categoria[ext.lower()] = categoria
    return extension_a_categoria

def es_carpeta_organizada(carpeta: Path, categorias: Dict[str, List[str]]) -> bool:
    """
    Verifica si una carpeta ya está organizada (contiene solo carpetas de categorías).
    
    Args:
        carpeta: Ruta de la carpeta a verificar
        categorias: Diccionario con categorías
        
    Returns:
        bool: True si la carpeta está organizada
    """
    if not carpeta.is_dir():
        return False
    
    # Obtener nombres de carpetas de categorías
    nombres_categorias = set(categorias.keys())
    
    # Verificar si todos los elementos son carpetas de categorías
    elementos = list(carpeta.iterdir())
    if not elementos:
        return False
    
    for elemento in elementos:
        if elemento.is_file():
            return False  # Si hay archivos, no está organizada
        if elemento.name not in nombres_categorias:
            return False  # Si hay carpetas que no son categorías, no está organizada
    
    return True

def organizar_recursivo(carpeta_objetivo: Path, 
                       categorias: Dict[str, List[str]] = None,
                       profundidad_maxima: int = 3,
                       evitar_organizadas: bool = True,
                       profundidad_actual: int = 0) -> Dict[str, int]:
    """
    Organiza archivos recursivamente en una carpeta y sus subcarpetas.
    
    Args:
        carpeta_objetivo: Ruta de la carpeta a organizar
        categorias: Diccionario con categorías y extensiones
        profundidad_maxima: Profundidad máxima de recursión
        evitar_organizadas: Si evitar carpetas ya organizadas
        profundidad_actual: Profundidad actual de recursión
        
    Returns:
        Dict[str, int]: Estadísticas de archivos movidos por categoría
    """
    if categorias is None:
        categorias = definir_categorias()
    
    if profundidad_actual > profundidad_maxima:
        return {}
    
    # Verificar que la carpeta existe
    if not carpeta_objetivo.exists() or not carpeta_objetivo.is_dir():
        return {}
    
    # Evitar carpetas ya organizadas
    if evitar_organizadas and es_carpeta_organizada(carpeta_objetivo, categorias):
        print(f"Saltando carpeta ya organizada: {carpeta_objetivo}")
        return {}
    
    extension_a_categoria = crear_diccionario_extensiones(categorias)
    estadisticas = {categoria: 0 for categoria in categorias.keys()}
    
    # Obtener todos los elementos (archivos y carpetas)
    elementos = list(carpeta_objetivo.iterdir())
    
    if not elementos:
        return estadisticas
    
    print(f"{'  ' * profundidad_actual}📁 Procesando: {carpeta_objetivo.name}")
    
    # Procesar archivos en esta carpeta
    archivos = [e for e in elementos if e.is_file()]
    for archivo in archivos:
        extension = archivo.suffix.lower()
        categoria = extension_a_categoria.get(extension, "Otros")
        carpeta_destino = carpeta_objetivo / categoria
        
        try:
            carpeta_destino.mkdir(exist_ok=True)
            
            # Manejar archivos duplicados
            archivo_destino = carpeta_destino / archivo.name
            if archivo_destino.exists():
                contador = 1
                nombre_base = archivo.stem
                extension_archivo = archivo.suffix
                while archivo_destino.exists():
                    nuevo_nombre = f"{nombre_base}_{contador}{extension_archivo}"
                    archivo_destino = carpeta_destino / nuevo_nombre
                    contador += 1
            
            archivo.rename(archivo_destino)
            print(f"{'  ' * profundidad_actual}  ✓ {archivo.name} → {categoria}/")
            estadisticas[categoria] += 1
            
        except Exception as e:
            print(f"{'  ' * profundidad_actual}  ✗ Error con {archivo.name}: {e}")
    
    # Procesar subcarpetas recursivamente
    subcarpetas = [e for e in elementos if e.is_dir() and e.name not in categorias.keys()]
    for subcarpeta in subcarpetas:
        stats_subcarpeta = organizar_recursivo(
            subcarpeta, 
            categorias, 
            profundidad_maxima, 
            evitar_organizadas, 
            profundidad_actual + 1
        )
        
        # Sumar estadísticas
        for categoria, cantidad in stats_subcarpeta.items():
            estadisticas[categoria] += cantidad
    
    return estadisticas

def main():
    """Función principal con opciones de configuración."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Organizador de archivos recursivo")
    parser.add_argument("--carpeta", "-c", type=str, 
                       default=str(Path.home() / "Downloads"),
                       help="Carpeta a organizar (default: Downloads)")
    parser.add_argument("--profundidad", "-p", type=int, default=3,
                       help="Profundidad máxima de recursión (default: 3)")
    parser.add_argument("--no-evitar-organizadas", action="store_true",
                       help="No evitar carpetas ya organizadas")
    parser.add_argument("--categorias-personalizadas", "-cat", type=str,
                       help="Archivo JSON con categorías personalizadas")
    
    args = parser.parse_args()
    
    carpeta_objetivo = Path(args.carpeta)
    
    if not carpeta_objetivo.exists():
        print(f"Error: La carpeta {carpeta_objetivo} no existe.")
        return
    
    print(f"🚀 Iniciando organización recursiva...")
    print(f"📁 Carpeta objetivo: {carpeta_objetivo}")
    print(f"🔍 Profundidad máxima: {args.profundidad}")
    print(f"🛡️  Evitar organizadas: {not args.no_evitar_organizadas}")
    print("="*60)
    
    # Cargar categorías personalizadas si se especifica
    categorias = None
    if args.categorias_personalizadas:
        import json
        try:
            with open(args.categorias_personalizadas, 'r', encoding='utf-8') as f:
                categorias = json.load(f)
            print(f"📋 Categorías cargadas desde: {args.categorias_personalizadas}")
        except Exception as e:
            print(f"Error al cargar categorías personalizadas: {e}")
            print("Usando categorías por defecto.")
    
    # Ejecutar organización
    estadisticas = organizar_recursivo(
        carpeta_objetivo,
        categorias,
        args.profundidad,
        not args.no_evitar_organizadas
    )
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE ORGANIZACIÓN RECURSIVA:")
    print("="*60)
    
    total_archivos = sum(estadisticas.values())
    if total_archivos > 0:
        print(f"✅ Total de archivos organizados: {total_archivos}")
        print("\n📁 Archivos por categoría:")
        for categoria, cantidad in estadisticas.items():
            if cantidad > 0:
                print(f"  {categoria}: {cantidad} archivos")
    else:
        print("ℹ️  No se encontraron archivos para organizar.")
    
    print(f"\n🎉 ¡Organización recursiva completada!")

if __name__ == "__main__":
    main() 