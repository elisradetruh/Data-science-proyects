# 🗂️ Organizador de Archivos Avanzado

Un conjunto de scripts Python para organizar automáticamente archivos en carpetas según su tipo de extensión.

## 📁 Archivos del Proyecto

- **`organizar.py`** - Script básico de organización
- **`organizar_recursivo.py`** - Organización recursiva en subcarpetas
- **`organizar_avanzado.py`** - Versión avanzada con notificaciones y configuración
- **`organizar_gui.py`** - 🆕 **Interfaz gráfica** con tkinter
- **`revertir_organizacion.py`** - Revertir la organización (modo educativo)
- **`config_organizador.json`** - Archivo de configuración (se crea automáticamente)

## 🚀 Instalación

### Requisitos
```bash
# Módulos básicos (incluidos con Python)
# - pathlib (Python 3.4+)
# - tkinter (incluido con Python)
# - argparse (incluido con Python)
```

### Para notificaciones (opcional)
```bash
# Windows
pip install win10toast

# macOS
brew install terminal-notifier

# Linux
sudo apt-get install libnotify-bin
```

## 📖 Uso Básico

### 1. 🖥️ Interfaz Gráfica (Recomendado para principiantes)
```bash
python organizar_gui.py
```
- **Interfaz visual** fácil de usar
- **Selector de carpeta** con botón "Examinar"
- **Opciones configurables** con checkboxes
- **Log en tiempo real** con barra de progreso
- **Simulación** sin mover archivos
- **Estadísticas visuales** de la carpeta

### 2. Organización Simple (Línea de comandos)
```bash
python organizar.py
```
Organiza archivos en la carpeta Downloads del usuario.

### 3. Organización Recursiva
```bash
python organizar_recursivo.py
python organizar_recursivo.py --carpeta "C:/MiCarpeta"
python organizar_recursivo.py --profundidad 5
```

### 4. Organización Avanzada
```bash
# Organizar con notificaciones
python organizar_avanzado.py

# Carpeta específica
python organizar_avanzado.py -c "C:/MiCarpeta"

# Sobrescribir archivos duplicados
python organizar_avanzado.py --sobrescribir

# Sin notificaciones
python organizar_avanzado.py --no-notificaciones

# Crear archivo de configuración
python organizar_avanzado.py --crear-config
```

### 5. Revertir Organización
```bash
# Simular reversión (preview)
python revertir_organizacion.py --simular

# Revertir organización
python revertir_organizacion.py

# Revertir sin eliminar carpetas vacías
python revertir_organizacion.py --no-eliminar
```

## ⚙️ Configuración

### Archivo de Configuración (`config_organizador.json`)
```json
{
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
    "sobrescribir": false,
    "recursivo": false,
    "profundidad_maxima": 3,
    "evitar_organizadas": true,
    "notificaciones": true,
    "crear_log": true
  },
  "carpetas_por_defecto": {
    "windows": "Downloads",
    "macos": "Downloads",
    "linux": "Downloads"
  }
}
```

### Personalizar Categorías
Puedes crear tu propio archivo de configuración:
```bash
python organizar_avanzado.py --crear-config mi_config.json
```

## 🔧 Opciones Avanzadas

### 🖥️ Interfaz Gráfica (organizar_gui.py)

#### Características principales:
- **Selector de carpeta**: Botón "Examinar" para elegir carpeta
- **Opciones configurables**:
  - ✅ Sobrescribir archivos duplicados
  - ✅ Mostrar notificaciones del sistema
  - ✅ Crear archivo de log
- **Botones de acción**:
  - 🚀 **Organizar Archivos**: Ejecuta la organización
  - 🔍 **Simular**: Muestra qué se haría sin mover archivos
  - ⚙️ **Configuración**: Ventana de configuración avanzada
  - 📊 **Estadísticas**: Muestra estadísticas de la carpeta
- **Log en tiempo real**: Área de texto con scroll y timestamps
- **Barra de progreso**: Indicador visual durante la organización
- **Gestión de logs**: Botones para limpiar y guardar logs

### Argumentos de Línea de Comandos

#### Organizador Avanzado
- `--carpeta, -c`: Carpeta a organizar
- `--config`: Archivo de configuración JSON
- `--sobrescribir`: Sobrescribir archivos duplicados
- `--recursivo, -r`: Organizar subcarpetas recursivamente
- `--profundidad, -p`: Profundidad máxima para recursión
- `--no-notificaciones`: Deshabilitar notificaciones
- `--no-log`: No crear archivo de log
- `--crear-config`: Crear archivo de configuración por defecto
- `--mostrar-config`: Mostrar configuración actual

#### Organizador Recursivo
- `--carpeta, -c`: Carpeta a organizar
- `--profundidad, -p`: Profundidad máxima de recursión
- `--no-evitar-organizadas`: No evitar carpetas ya organizadas
- `--categorias-personalizadas, -cat`: Archivo JSON con categorías

#### Revertir Organización
- `--carpeta, -c`: Carpeta a revertir
- `--simular, -s`: Simular reversión sin mover archivos
- `--no-eliminar`: No eliminar carpetas vacías
- `--no-log`: No crear archivo de log
- `--confirmar`: Confirmar reversión sin preguntar

## 📊 Logs y Estadísticas

### Archivos de Log
- `organizador.log`: Log de archivos movidos
- `reversion_organizador.log`: Log de reversiones

### Ejemplo de Log
```
[2024-01-15 14:30:25] MOVED: documento.pdf → C:/Downloads/Documentos/
[2024-01-15 14:30:26] MOVED: imagen.jpg → C:/Downloads/Imagenes/
[2024-01-15 14:30:27] REVERTED: documento.pdf (Documentos) → C:/Downloads/
```

## 🔄 Programación Automática

### Windows (Tareas Programadas)
1. Abrir "Programador de tareas"
2. Crear tarea básica
3. Programar para ejecutar:
```cmd
python C:\ruta\al\organizar_avanzado.py
```

### macOS/Linux (Cron)
```bash
# Editar crontab
crontab -e

# Ejecutar cada día a las 8:00 AM
0 8 * * * /usr/bin/python3 /ruta/al/organizar_avanzado.py

# Ejecutar cada hora
0 * * * * /usr/bin/python3 /ruta/al/organizar_avanzado.py
```

### Crear Ejecutable (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile organizar_avanzado.py
```

## 🛡️ Características de Seguridad

### Prevención de Pérdida de Datos
- ✅ Verificación de existencia de carpetas
- ✅ Manejo de archivos duplicados
- ✅ Modo simulación disponible
- ✅ Logs detallados de todas las acciones
- ✅ Confirmación antes de operaciones destructivas

### Carpetas Protegidas
El script evita automáticamente:
- Carpetas del sistema
- Carpetas ya organizadas (en modo recursivo)
- Carpetas de categorías existentes

## 🎯 Casos de Uso

### 1. 🖥️ Uso Diario con Interfaz Gráfica
```bash
# Para usuarios principiantes o uso diario
python organizar_gui.py
```
- Seleccionar carpeta con el botón "Examinar"
- Configurar opciones con checkboxes
- Hacer clic en "Simular" para ver qué pasará
- Hacer clic en "Organizar Archivos" para ejecutar
- Ver resultados en tiempo real en el log

### 2. Organización Automática (Línea de comandos)
```bash
# Organizar Downloads automáticamente
python organizar_avanzado.py --confirmar
```

### 3. Limpieza de Proyectos
```bash
# Organizar carpeta de proyecto recursivamente
python organizar_recursivo.py -c "C:/Proyectos/MiProyecto" -p 5
```

### 4. Backup y Restauración
```bash
# Hacer backup antes de organizar
cp -r Downloads Downloads_backup

# Organizar
python organizar_avanzado.py

# Revertir si es necesario
python revertir_organizacion.py
```

### 5. Configuración Personalizada
```json
{
  "categorias": {
    "Codigo": [".py", ".js", ".html", ".css", ".java"],
    "Datos": [".csv", ".json", ".xml", ".sql"],
    "Presentaciones": [".ppt", ".pptx", ".key"],
    "Otros": []
  }
}
```

## 🐛 Solución de Problemas

### Error: "Carpeta no existe"
- Verificar que la ruta sea correcta
- Usar rutas absolutas en Windows: `C:/Users/Usuario/Downloads`
- En la GUI, usar el botón "Examinar" para seleccionar carpeta

### Error: "Permisos denegados"
- Ejecutar como administrador (Windows)
- Verificar permisos de la carpeta
- Cerrar programas que puedan estar usando los archivos

### Error: "tkinter no está disponible"
- En Linux: `sudo apt-get install python3-tk`
- En macOS: `brew install python-tk`
- En Windows: tkinter viene incluido con Python

### Notificaciones no funcionan
- Instalar dependencias necesarias:
  - Windows: `pip install win10toast`
  - macOS: `brew install terminal-notifier`
  - Linux: `sudo apt-get install libnotify-bin`

### Archivos no se mueven
- Verificar que no estén en uso
- Comprobar espacio en disco
- Revisar permisos de escritura
- Usar la función "Simular" para ver qué archivos causan problemas

### La GUI no responde durante la organización
- Es normal, la organización se ejecuta en un hilo separado
- La barra de progreso indica que está trabajando
- Esperar a que termine la operación

## 📝 Contribuir

1. Fork el proyecto
2. Crear rama para nueva funcionalidad
3. Commit cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Soporte

Para reportar bugs o solicitar funcionalidades:
- Crear un issue en GitHub
- Incluir información del sistema operativo
- Adjuntar logs de error si es posible

## 🆕 Novedades en la Versión Actual

### ✨ Nueva Interfaz Gráfica
- **`organizar_gui.py`**: Interfaz visual completa con tkinter
- **Fácil de usar**: Botones, checkboxes y selector de carpetas
- **Log en tiempo real**: Ver el progreso mientras organiza
- **Simulación**: Probar antes de ejecutar
- **Estadísticas visuales**: Información detallada de la carpeta

### 🔄 Comparación de Interfaces

| Característica | GUI | Línea de Comandos |
|----------------|-----|-------------------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Velocidad** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Opciones avanzadas** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Visualización** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Automatización** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### 🎯 Recomendaciones de Uso
- **Principiantes**: Usar `organizar_gui.py`
- **Usuarios avanzados**: Usar `organizar_avanzado.py`
- **Automatización**: Usar scripts de línea de comandos
- **Proyectos grandes**: Usar `organizar_recursivo.py`

---

**¡Disfruta organizando tus archivos de manera automática! 🎉** 