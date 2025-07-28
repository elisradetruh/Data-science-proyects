import os
import shutil
import json
import argparse
import platform
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

def enviar_notificacion(titulo: str, mensaje: str, sistema: str = None):
    """
    Envía una notificación del sistema según el OS.
    
    Args:
        titulo: Título de la notificación
        mensaje: Mensaje de la notificación
        sistema: Sistema operativo (auto-detectado si es None)
    """
    if sistema is None:
        sistema = platform.system()
    
    try:
        if sistema == "Windows":
            # Windows - usando win10toast o plyer
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(titulo, mensaje, duration=5)
            except ImportError:
                # Fallback usando PowerShell
                ps_script = f'''
                Add-Type -AssemblyName System.Windows.Forms
                $notification = New-Object System.Windows.Forms.NotifyIcon
                $notification.Icon = [System.Drawing.SystemIcons]::Information
                $notification.BalloonTipTitle = "{titulo}"
                $notification.BalloonTipText = "{mensaje}"
                $notification.Visible = $true
                $notification.ShowBalloonTip(5000)
                '''
                os.system(f'powershell -Command "{ps_script}"')
                
        elif sistema == "Darwin":  # macOS
            # macOS - usando terminal-notifier o osascript
            osascript = f'''
            display notification "{mensaje}" with title "{titulo}"
            '''
            os.system(f"osascript -e '{osascript}'")
            
        elif sistema == "Linux":
            # Linux - usando notify-send
            os.system(f'notify-send "{titulo}" "{mensaje}"')
            
        else:
            print(f"⚠️  Notificaciones no soportadas en {sistema}")
            
    except Exception as e:
        print(f"Error al enviar notificación: {e}")

def cargar_configuracion(archivo_config: str = "config_organizador.json") -> Dict:
    """
    Carga configuración desde archivo JSON.
    
    Args:
        archivo_config: Ruta del archivo de configuración
        
    Returns:
        Dict: Configuración cargada
    """
    config_default = {
        "categorias": {
            "Imagenes": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
            "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".doc", ".rtf", ".odt"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
            "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Programas": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
            "Otros": []
        },
        "opciones": {
            "sobrescribir": False,
            "recursivo": False,
            "profundidad_maxima": 3,
            "evitar_organizadas": True,
            "notificaciones": True,
            "crear_log": True
        },
        "carpetas_por_defecto": {
            "windows": "Downloads",
            "macos": "Downloads", 
            "linux": "Downloads"
        }
    }
    
    try:
        with open(archivo_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Combinar con configuración por defecto
            for key, value in config_default.items():
                if key not in config:
                    config[key] = value
            return config
    except FileNotFoundError:
        print(f"📝 Archivo de configuración no encontrado. Creando {archivo_config}...")
        guardar_configuracion(config_default, archivo_config)
        return config_default
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
        return config_default

def guardar_configuracion(config: Dict, archivo_config: str = "config_organizador.json"):
    """Guarda configuración en archivo JSON."""
    try:
        with open(archivo_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuración guardada en {archivo_config}")
    except Exception as e:
        print(f"Error al guardar configuración: {e}")

def crear_log(archivo: str, accion: str, origen: str, destino: str):
    """Crea un log de las acciones realizadas."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {accion}: {origen} → {destino}\n"
    
    try:
        with open("organizador.log", "a", encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error al escribir log: {e}")

def organizar_archivos_avanzado(carpeta_objetivo: Path, 
                               config: Dict,
                               crear_log_archivos: bool = True) -> Dict[str, int]:
    """
    Organiza archivos con opciones avanzadas.
    
    Args:
        carpeta_objetivo: Carpeta a organizar
        config: Configuración del organizador
        crear_log_archivos: Si crear log de archivos
        
    Returns:
        Dict[str, int]: Estadísticas de archivos movidos
    """
    categorias = config["categorias"]
    opciones = config["opciones"]
    
    # Crear diccionario de extensiones
    extension_a_categoria = {}
    for categoria, extensiones in categorias.items():
        for ext in extensiones:
            extension_a_categoria[ext.lower()] = categoria
    
    # Verificar carpeta
    if not carpeta_objetivo.exists():
        print(f"❌ Error: La carpeta {carpeta_objetivo} no existe.")
        return {}
    
    if not carpeta_objetivo.is_dir():
        print(f"❌ Error: {carpeta_objetivo} no es una carpeta.")
        return {}
    
    # Obtener archivos
    archivos = [f for f in carpeta_objetivo.iterdir() if f.is_file()]
    
    if not archivos:
        print(f"ℹ️  No se encontraron archivos en {carpeta_objetivo}")
        return {}
    
    estadisticas = {categoria: 0 for categoria in categorias.keys()}
    archivos_movidos = 0
    archivos_omitidos = 0
    
    print(f"🚀 Organizando {len(archivos)} archivos...")
    
    for archivo in archivos:
        extension = archivo.suffix.lower()
        categoria = extension_a_categoria.get(extension, "Otros")
        carpeta_destino = carpeta_objetivo / categoria
        
        try:
            carpeta_destino.mkdir(exist_ok=True)
            archivo_destino = carpeta_destino / archivo.name
            
            # Manejar archivos duplicados
            if archivo_destino.exists():
                if opciones["sobrescribir"]:
                    archivo_destino.unlink()  # Eliminar archivo existente
                else:
                    # Renombrar con número
                    contador = 1
                    nombre_base = archivo.stem
                    extension_archivo = archivo.suffix
                    while archivo_destino.exists():
                        nuevo_nombre = f"{nombre_base}_{contador}{extension_archivo}"
                        archivo_destino = carpeta_destino / nuevo_nombre
                        contador += 1
            
            # Mover archivo
            archivo.rename(archivo_destino)
            
            # Crear log si está habilitado
            if crear_log_archivos and opciones["crear_log"]:
                crear_log(archivo.name, "MOVED", str(archivo), str(archivo_destino))
            
            print(f"  ✓ {archivo.name} → {categoria}/")
            estadisticas[categoria] += 1
            archivos_movidos += 1
            
        except Exception as e:
            print(f"  ✗ Error con {archivo.name}: {e}")
            archivos_omitidos += 1
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print("📊 RESUMEN:")
    print(f"{'='*50}")
    print(f"✅ Archivos movidos: {archivos_movidos}")
    print(f"⚠️  Archivos omitidos: {archivos_omitidos}")
    print(f"📁 Total procesados: {len(archivos)}")
    
    if archivos_movidos > 0:
        print(f"\n📂 Archivos por categoría:")
        for categoria, cantidad in estadisticas.items():
            if cantidad > 0:
                print(f"  {categoria}: {cantidad} archivos")
    
    return estadisticas

def main():
    """Función principal con interfaz avanzada."""
    parser = argparse.ArgumentParser(
        description="Organizador de archivos avanzado con notificaciones",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python organizar_avanzado.py                    # Organizar Downloads
  python organizar_avanzado.py -c "C:/MiCarpeta"  # Carpeta específica
  python organizar_avanzado.py --sobrescribir     # Sobrescribir duplicados
  python organizar_avanzado.py --config mi_config.json  # Configuración personalizada
  python organizar_avanzado.py --no-notificaciones      # Sin notificaciones
        """
    )
    
    parser.add_argument("--carpeta", "-c", type=str,
                       help="Carpeta a organizar (default: Musica)")
    parser.add_argument("--config", type=str, default="config_organizador.json",
                       help="Archivo de configuración JSON")
    parser.add_argument("--sobrescribir", action="store_true",
                       help="Sobrescribir archivos duplicados")
    parser.add_argument("--recursivo", "-r", action="store_true",
                       help="Organizar subcarpetas recursivamente")
    parser.add_argument("--profundidad", "-p", type=int, default=3,
                       help="Profundidad máxima para recursión")
    parser.add_argument("--no-notificaciones", action="store_true",
                       help="Deshabilitar notificaciones")
    parser.add_argument("--no-log", action="store_true",
                       help="No crear archivo de log")
    parser.add_argument("--crear-config", action="store_true",
                       help="Crear archivo de configuración por defecto")
    parser.add_argument("--mostrar-config", action="store_true",
                       help="Mostrar configuración actual")
    
    args = parser.parse_args()
    
    # Cargar configuración
    config = cargar_configuracion(args.config)
    
    # Crear configuración por defecto si se solicita
    if args.crear_config:
        guardar_configuracion(config, args.config)
        return
    
    # Mostrar configuración si se solicita
    if args.mostrar_config:
        print("📋 Configuración actual:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return
    
    # Determinar carpeta objetivo
    if args.carpeta:
        carpeta_objetivo = Path(args.carpeta)
    else:
        sistema = platform.system().lower()
        carpeta_default = config["carpetas_por_defecto"].get(sistema, "Downloads")
        carpeta_objetivo = Path.home() / carpeta_default
    
    # Actualizar configuración con argumentos de línea de comandos
    if args.sobrescribir:
        config["opciones"]["sobrescribir"] = True
    if args.recursivo:
        config["opciones"]["recursivo"] = True
    if args.profundidad:
        config["opciones"]["profundidad_maxima"] = args.profundidad
    if args.no_notificaciones:
        config["opciones"]["notificaciones"] = False
    if args.no_log:
        config["opciones"]["crear_log"] = False
    
    # Verificar carpeta
    if not carpeta_objetivo.exists():
        print(f"❌ Error: La carpeta {carpeta_objetivo} no existe.")
        return
    
    print(f"🚀 Organizador de archivos avanzado")
    print(f"📁 Carpeta: {carpeta_objetivo}")
    print(f"⚙️  Configuración: {args.config}")
    print(f"🔄 Recursivo: {config['opciones']['recursivo']}")
    print(f"📝 Log: {config['opciones']['crear_log']}")
    print("="*60)
    
    # Ejecutar organización
    inicio = datetime.now()
    estadisticas = organizar_archivos_avanzado(
        carpeta_objetivo, 
        config, 
        not args.no_log
    )
    fin = datetime.now()
    
    # Calcular tiempo de ejecución
    tiempo_ejecucion = (fin - inicio).total_seconds()
    
    # Enviar notificación si está habilitada
    if config["opciones"]["notificaciones"] and not args.no_notificaciones:
        total_archivos = sum(estadisticas.values())
        if total_archivos > 0:
            titulo = "✅ Organización completada"
            mensaje = f"Se organizaron {total_archivos} archivos en {tiempo_ejecucion:.1f}s"
        else:
            titulo = "ℹ️ Organización completada"
            mensaje = "No se encontraron archivos para organizar"
        
        enviar_notificacion(titulo, mensaje)
    
    print(f"\n⏱️  Tiempo de ejecución: {tiempo_ejecucion:.2f} segundos")
    print(f"🎉 ¡Organización completada!")

if __name__ == "__main__":
    main() 