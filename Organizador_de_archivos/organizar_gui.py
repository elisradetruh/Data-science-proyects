import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
from pathlib import Path
from datetime import datetime
import sys
import io

# Importar funciones del organizador avanzado
try:
    from organizar_avanzado import (
        cargar_configuracion, 
        guardar_configuracion, 
        organizar_archivos_avanzado,
        enviar_notificacion
    )
except ImportError:
    # Si no está disponible, crear funciones básicas
    def cargar_configuracion(archivo="config_organizador.json"):
        return {
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
            }
        }
    
    def guardar_configuracion(config, archivo="config_organizador.json"):
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def organizar_archivos_avanzado(carpeta_objetivo, config, crear_log=True):
        # Función básica de organización
        categorias = config["categorias"]
        extension_a_categoria = {}
        for categoria, extensiones in categorias.items():
            for ext in extensiones:
                extension_a_categoria[ext.lower()] = categoria
        
        archivos = [f for f in carpeta_objetivo.iterdir() if f.is_file()]
        estadisticas = {categoria: 0 for categoria in categorias.keys()}
        
        for archivo in archivos:
            extension = archivo.suffix.lower()
            categoria = extension_a_categoria.get(extension, "Otros")
            carpeta_destino = carpeta_objetivo / categoria
            
            try:
                carpeta_destino.mkdir(exist_ok=True)
                archivo.rename(carpeta_destino / archivo.name)
                estadisticas[categoria] += 1
            except Exception as e:
                pass
        
        return estadisticas
    
    def enviar_notificacion(titulo, mensaje):
        pass

class OrganizadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🗂️ Organizador de Archivos")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configuración
        self.config = cargar_configuracion()
        self.carpeta_seleccionada = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.progreso = tk.StringVar(value="Listo para organizar")
        
        # Variables de control
        self.sobrescribir = tk.BooleanVar(value=False)
        self.notificaciones = tk.BooleanVar(value=True)
        self.crear_log = tk.BooleanVar(value=True)
        
        self.crear_interfaz()
        self.cargar_configuracion()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="🗂️ Organizador de Archivos", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de carpeta
        ttk.Label(main_frame, text="📁 Carpeta a organizar:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        carpeta_frame = ttk.Frame(main_frame)
        carpeta_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        carpeta_frame.columnconfigure(0, weight=1)
        
        self.entry_carpeta = ttk.Entry(carpeta_frame, textvariable=self.carpeta_seleccionada, width=50)
        self.entry_carpeta.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(carpeta_frame, text="Examinar", 
                  command=self.seleccionar_carpeta).grid(row=0, column=1)
        
        # Opciones
        opciones_frame = ttk.LabelFrame(main_frame, text="⚙️ Opciones", padding="10")
        opciones_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        opciones_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(opciones_frame, text="Sobrescribir archivos duplicados", 
                       variable=self.sobrescribir).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Checkbutton(opciones_frame, text="Mostrar notificaciones", 
                       variable=self.notificaciones).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Checkbutton(opciones_frame, text="Crear archivo de log", 
                       variable=self.crear_log).grid(row=1, column=0, sticky=tk.W)
        
        # Botones principales
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(botones_frame, text="🚀 Organizar Archivos", 
                  command=self.organizar_archivos, 
                  style="Accent.TButton").grid(row=0, column=0, padx=5)
        
        ttk.Button(botones_frame, text="🔍 Simular", 
                  command=self.simular_organizacion).grid(row=0, column=1, padx=5)
        
        ttk.Button(botones_frame, text="⚙️ Configuración", 
                  command=self.mostrar_configuracion).grid(row=0, column=2, padx=5)
        
        ttk.Button(botones_frame, text="📊 Estadísticas", 
                  command=self.mostrar_estadisticas).grid(row=0, column=3, padx=5)
        
        # Barra de progreso
        ttk.Label(main_frame, text="Estado:").grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        ttk.Label(main_frame, textvariable=self.progreso).grid(row=4, column=1, sticky=tk.W, pady=(20, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="📝 Log de Actividad", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones de log
        log_botones_frame = ttk.Frame(log_frame)
        log_botones_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(log_botones_frame, text="Limpiar Log", 
                  command=self.limpiar_log).grid(row=0, column=0, padx=5)
        
        ttk.Button(log_botones_frame, text="Guardar Log", 
                  command=self.guardar_log).grid(row=0, column=1, padx=5)
    
    def seleccionar_carpeta(self):
        """Permite al usuario seleccionar una carpeta."""
        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta a organizar",
            initialdir=self.carpeta_seleccionada.get()
        )
        if carpeta:
            self.carpeta_seleccionada.set(carpeta)
    
    def cargar_configuracion(self):
        """Carga la configuración actual."""
        try:
            self.config = cargar_configuracion()
            self.sobrescribir.set(self.config["opciones"]["sobrescribir"])
            self.notificaciones.set(self.config["opciones"]["notificaciones"])
            self.crear_log.set(self.config["opciones"]["crear_log"])
        except Exception as e:
            self.log(f"Error al cargar configuración: {e}")
    
    def organizar_archivos(self):
        """Ejecuta la organización de archivos en un hilo separado."""
        if not self.validar_carpeta():
            return
        
        # Deshabilitar botones durante la operación
        self.progreso.set("Organizando archivos...")
        self.progress_bar.start()
        
        # Ejecutar en hilo separado para no bloquear la GUI
        thread = threading.Thread(target=self._organizar_archivos_thread)
        thread.daemon = True
        thread.start()
    
    def _organizar_archivos_thread(self):
        """Hilo para organizar archivos."""
        try:
            carpeta_objetivo = Path(self.carpeta_seleccionada.get())
            
            # Actualizar configuración con opciones de la GUI
            self.config["opciones"]["sobrescribir"] = self.sobrescribir.get()
            self.config["opciones"]["notificaciones"] = self.notificaciones.get()
            self.config["opciones"]["crear_log"] = self.crear_log.get()
            
            # Redirigir stdout para capturar la salida
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            # Ejecutar organización
            estadisticas = organizar_archivos_avanzado(
                carpeta_objetivo, 
                self.config, 
                self.crear_log.get()
            )
            
            # Obtener salida capturada
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Actualizar GUI en el hilo principal
            self.root.after(0, self._finalizar_organizacion, estadisticas, output)
            
        except Exception as e:
            self.root.after(0, self._mostrar_error, str(e))
    
    def _finalizar_organizacion(self, estadisticas, output):
        """Finaliza la organización y actualiza la GUI."""
        self.progress_bar.stop()
        
        # Mostrar salida en el log
        self.log(output)
        
        # Calcular estadísticas
        total_archivos = sum(estadisticas.values())
        
        if total_archivos > 0:
            self.progreso.set(f"✅ Organización completada - {total_archivos} archivos movidos")
            self.log(f"\n📊 RESUMEN:")
            for categoria, cantidad in estadisticas.items():
                if cantidad > 0:
                    self.log(f"  {categoria}: {cantidad} archivos")
            
            # Mostrar notificación
            if self.notificaciones.get():
                enviar_notificacion(
                    "✅ Organización completada",
                    f"Se organizaron {total_archivos} archivos"
                )
        else:
            self.progreso.set("ℹ️ No se encontraron archivos para organizar")
    
    def _mostrar_error(self, error):
        """Muestra un error en la GUI."""
        self.progress_bar.stop()
        self.progreso.set("❌ Error en la organización")
        self.log(f"❌ ERROR: {error}")
        messagebox.showerror("Error", f"Error al organizar archivos:\n{error}")
    
    def simular_organizacion(self):
        """Simula la organización sin mover archivos."""
        if not self.validar_carpeta():
            return
        
        carpeta_objetivo = Path(self.carpeta_seleccionada.get())
        archivos = [f for f in carpeta_objetivo.iterdir() if f.is_file()]
        
        if not archivos:
            messagebox.showinfo("Simulación", "No se encontraron archivos para organizar.")
            return
        
        # Contar archivos por categoría
        categorias = self.config["categorias"]
        extension_a_categoria = {}
        for categoria, extensiones in categorias.items():
            for ext in extensiones:
                extension_a_categoria[ext.lower()] = categoria
        
        estadisticas = {categoria: 0 for categoria in categorias.keys()}
        
        for archivo in archivos:
            extension = archivo.suffix.lower()
            categoria = extension_a_categoria.get(extension, "Otros")
            estadisticas[categoria] += 1
        
        # Mostrar resultados
        resultado = "🔍 SIMULACIÓN DE ORGANIZACIÓN\n"
        resultado += f"📁 Carpeta: {carpeta_objetivo}\n"
        resultado += f"📊 Total de archivos: {len(archivos)}\n\n"
        resultado += "📂 Archivos por categoría:\n"
        
        for categoria, cantidad in estadisticas.items():
            if cantidad > 0:
                resultado += f"  {categoria}: {cantidad} archivos\n"
        
        self.log(resultado)
        messagebox.showinfo("Simulación", resultado)
    
    def mostrar_configuracion(self):
        """Muestra la ventana de configuración."""
        config_window = tk.Toplevel(self.root)
        config_window.title("⚙️ Configuración")
        config_window.geometry("600x400")
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Crear interfaz de configuración
        self.crear_ventana_configuracion(config_window)
    
    def crear_ventana_configuracion(self, window):
        """Crea la interfaz de la ventana de configuración."""
        notebook = ttk.Notebook(window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de categorías
        categorias_frame = ttk.Frame(notebook)
        notebook.add(categorias_frame, text="📂 Categorías")
        
        # Pestaña de opciones
        opciones_frame = ttk.Frame(notebook)
        notebook.add(opciones_frame, text="⚙️ Opciones")
        
        # Implementar contenido de las pestañas
        self.crear_pestana_categorias(categorias_frame)
        self.crear_pestana_opciones(opciones_frame)
    
    def crear_pestana_categorias(self, parent):
        """Crea la pestaña de configuración de categorías."""
        # Implementación básica
        ttk.Label(parent, text="Configuración de categorías").pack(pady=20)
        ttk.Label(parent, text="(Funcionalidad en desarrollo)").pack()
    
    def crear_pestana_opciones(self, parent):
        """Crea la pestaña de configuración de opciones."""
        # Implementación básica
        ttk.Label(parent, text="Configuración de opciones").pack(pady=20)
        ttk.Label(parent, text="(Funcionalidad en desarrollo)").pack()
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de la carpeta seleccionada."""
        if not self.validar_carpeta():
            return
        
        carpeta_objetivo = Path(self.carpeta_seleccionada.get())
        archivos = [f for f in carpeta_objetivo.iterdir() if f.is_file()]
        
        if not archivos:
            messagebox.showinfo("Estadísticas", "No se encontraron archivos.")
            return
        
        # Calcular estadísticas
        total_archivos = len(archivos)
        total_tamaño = sum(f.stat().st_size for f in archivos)
        
        # Contar por extensión
        extensiones = {}
        for archivo in archivos:
            ext = archivo.suffix.lower()
            extensiones[ext] = extensiones.get(ext, 0) + 1
        
        # Mostrar resultados
        stats = f"📊 ESTADÍSTICAS DE LA CARPETA\n"
        stats += f"📁 Carpeta: {carpeta_objetivo}\n"
        stats += f"📄 Total de archivos: {total_archivos}\n"
        stats += f"💾 Tamaño total: {total_tamaño / (1024*1024):.2f} MB\n\n"
        stats += "📂 Archivos por extensión:\n"
        
        for ext, cantidad in sorted(extensiones.items(), key=lambda x: x[1], reverse=True):
            stats += f"  {ext or 'Sin extensión'}: {cantidad} archivos\n"
        
        self.log(stats)
        messagebox.showinfo("Estadísticas", stats)
    
    def validar_carpeta(self):
        """Valida que la carpeta seleccionada existe."""
        carpeta = Path(self.carpeta_seleccionada.get())
        if not carpeta.exists():
            messagebox.showerror("Error", f"La carpeta {carpeta} no existe.")
            return False
        if not carpeta.is_dir():
            messagebox.showerror("Error", f"{carpeta} no es una carpeta.")
            return False
        return True
    
    def log(self, mensaje):
        """Agrega un mensaje al log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.log_text.see(tk.END)
    
    def limpiar_log(self):
        """Limpia el área de log."""
        self.log_text.delete(1.0, tk.END)
    
    def guardar_log(self):
        """Guarda el log en un archivo."""
        archivo = filedialog.asksaveasfilename(
            title="Guardar log",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Éxito", f"Log guardado en {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el log: {e}")

def main():
    """Función principal."""
    root = tk.Tk()
    
    # Configurar estilo
    style = ttk.Style()
    style.theme_use('clam')  # o 'vista' en Windows
    
    app = OrganizadorGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 