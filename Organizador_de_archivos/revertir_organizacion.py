import os
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

def definir_categorias() -> Dict[str, List[str]]:
    """Define las categorías de archivos (debe coincidir con el organizador)."""
    return {
        "Imagenes": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
        "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".doc", ".rtf", ".odt"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
        "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Programas": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
        "Otros": []
    }

def revertir_organizacion(carpeta_objetivo: Path, 
                         categorias: Dict[str, List[str]] = None,
                         eliminar_carpetas_vacias: bool = True,
                         crear_log: bool = True) -> Dict[str, int]:
    """
    Revierte la organización moviendo todos los archivos de vuelta a la carpeta principal.
    
    Args:
        carpeta_objetivo: Carpeta donde están las subcarpetas organizadas
        categorias: Diccionario con categorías (opcional)
        eliminar_carpetas_vacias: Si eliminar carpetas vacías después
        crear_log: Si crear log de acciones
        
    Returns:
        Dict[str, int]: Estadísticas de archivos movidos
    """
    if categorias is None:
        categorias = definir_categorias()
    
    # Verificar que la carpeta existe
    if not carpeta_objetivo.exists() or not carpeta_objetivo.is_dir():
        print(f"❌ Error: La carpeta {carpeta_objetivo} no existe o no es una carpeta.")
        return {}
    
    estadisticas = {categoria: 0 for categoria in categorias.keys()}
    archivos_movidos = 0
    archivos_fallidos = 0
    carpetas_eliminadas = 0
    
    print(f"🔄 Revirtiendo organización en: {carpeta_objetivo}")
    
    # Procesar cada carpeta de categoría
    for categoria in categorias.keys():
        carpeta_categoria = carpeta_objetivo / categoria
        
        if not carpeta_categoria.exists():
            continue
        
        print(f"📁 Procesando carpeta: {categoria}")
        
        # Obtener todos los archivos en la carpeta de categoría
        archivos = [f for f in carpeta_categoria.iterdir() if f.is_file()]
        
        for archivo in archivos:
            try:
                # Mover archivo de vuelta a la carpeta principal
                destino = carpeta_objetivo / archivo.name
                
                # Manejar archivos duplicados
                if destino.exists():
                    contador = 1
                    nombre_base = archivo.stem
                    extension = archivo.suffix
                    while destino.exists():
                        nuevo_nombre = f"{nombre_base}_revertido_{contador}{extension}"
                        destino = carpeta_objetivo / nuevo_nombre
                        contador += 1
                
                # Mover archivo
                archivo.rename(destino)
                
                # Crear log si está habilitado
                if crear_log:
                    crear_log_reversion(archivo.name, categoria, str(archivo), str(destino))
                
                print(f"  ✓ {archivo.name} → carpeta principal")
                estadisticas[categoria] += 1
                archivos_movidos += 1
                
            except Exception as e:
                print(f"  ✗ Error con {archivo.name}: {e}")
                archivos_fallidos += 1
        
        # Eliminar carpeta vacía si está habilitado
        if eliminar_carpetas_vacias:
            try:
                archivos_restantes = [f for f in carpeta_categoria.iterdir() if f.is_file()]
                if not archivos_restantes:
                    carpeta_categoria.rmdir()
                    print(f"  🗑️  Carpeta {categoria} eliminada (vacía)")
                    carpetas_eliminadas += 1
            except Exception as e:
                print(f"  ⚠️  No se pudo eliminar carpeta {categoria}: {e}")
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print("📊 RESUMEN DE REVERSIÓN:")
    print(f"{'='*50}")
    print(f"✅ Archivos movidos: {archivos_movidos}")
    print(f"⚠️  Archivos con errores: {archivos_fallidos}")
    print(f"🗑️  Carpetas eliminadas: {carpetas_eliminadas}")
    
    if archivos_movidos > 0:
        print(f"\n📂 Archivos por categoría original:")
        for categoria, cantidad in estadisticas.items():
            if cantidad > 0:
                print(f"  {categoria}: {cantidad} archivos")
    
    return estadisticas

def crear_log_reversion(archivo: str, categoria: str, origen: str, destino: str):
    """Crea un log de las acciones de reversión."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] REVERTED: {archivo} ({categoria}) → {destino}\n"
    
    try:
        with open("reversion_organizador.log", "a", encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error al escribir log: {e}")

def simular_reversion(carpeta_objetivo: Path, categorias: Dict[str, List[str]] = None) -> Dict[str, int]:
    """
    Simula la reversión sin mover archivos (modo preview).
    
    Args:
        carpeta_objetivo: Carpeta a analizar
        categorias: Diccionario con categorías
        
    Returns:
        Dict[str, int]: Estadísticas simuladas
    """
    if categorias is None:
        categorias = definir_categorias()
    
    if not carpeta_objetivo.exists() or not carpeta_objetivo.is_dir():
        print(f"❌ Error: La carpeta {carpeta_objetivo} no existe.")
        return {}
    
    estadisticas = {categoria: 0 for categoria in categorias.keys()}
    total_archivos = 0
    
    print(f"🔍 Simulando reversión en: {carpeta_objetivo}")
    print("(Modo preview - no se moverán archivos)")
    
    for categoria in categorias.keys():
        carpeta_categoria = carpeta_objetivo / categoria
        
        if not carpeta_categoria.exists():
            continue
        
        archivos = [f for f in carpeta_categoria.iterdir() if f.is_file()]
        if archivos:
            print(f"📁 {categoria}: {len(archivos)} archivos")
            estadisticas[categoria] = len(archivos)
            total_archivos += len(archivos)
    
    print(f"\n📊 Total de archivos que se moverían: {total_archivos}")
    return estadisticas

def main():
    """Función principal para revertir organización."""
    parser = argparse.ArgumentParser(
        description="Revertir organización de archivos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python revertir_organizacion.py                    # Revertir Downloads
  python revertir_organizacion.py -c "C:/MiCarpeta"  # Carpeta específica
  python revertir_organizacion.py --simular          # Solo mostrar qué se haría
  python revertir_organizacion.py --no-eliminar      # No eliminar carpetas vacías
        """
    )
    
    parser.add_argument("--carpeta", "-c", type=str,
                       help="Carpeta a revertir (default: Downloads)")
    parser.add_argument("--simular", "-s", action="store_true",
                       help="Simular reversión sin mover archivos")
    parser.add_argument("--no-eliminar", action="store_true",
                       help="No eliminar carpetas vacías")
    parser.add_argument("--no-log", action="store_true",
                       help="No crear archivo de log")
    parser.add_argument("--confirmar", action="store_true",
                       help="Confirmar reversión sin preguntar")
    
    args = parser.parse_args()
    
    # Determinar carpeta objetivo
    if args.carpeta:
        carpeta_objetivo = Path(args.carpeta)
    else:
        carpeta_objetivo = Path.home() / "Downloads"
    
    # Verificar carpeta
    if not carpeta_objetivo.exists():
        print(f"❌ Error: La carpeta {carpeta_objetivo} no existe.")
        return
    
    categorias = definir_categorias()
    
    print(f"🔄 Revertir organización de archivos")
    print(f"📁 Carpeta: {carpeta_objetivo}")
    print(f"🔍 Modo: {'Simulación' if args.simular else 'Ejecución'}")
    print("="*60)
    
    # Simular o ejecutar
    if args.simular:
        estadisticas = simular_reversion(carpeta_objetivo, categorias)
    else:
        # Confirmar si no se especificó --confirmar
        if not args.confirmar:
            print("\n⚠️  ADVERTENCIA: Esta acción moverá todos los archivos de vuelta a la carpeta principal.")
            respuesta = input("¿Estás seguro de que quieres continuar? (s/N): ")
            if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Operación cancelada.")
                return
        
        # Ejecutar reversión
        estadisticas = revertir_organizacion(
            carpeta_objetivo,
            categorias,
            not args.no_eliminar,
            not args.no_log
        )
    
    # Mostrar resultado final
    total_archivos = sum(estadisticas.values())
    if total_archivos > 0:
        print(f"\n✅ {'Simulación completada' if args.simular else 'Reversión completada'}")
        print(f"📁 Total de archivos: {total_archivos}")
    else:
        print(f"\nℹ️  No se encontraron archivos organizados para revertir.")

if __name__ == "__main__":
    main() 