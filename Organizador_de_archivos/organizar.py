#TODO: La automatización de tareas repetitivas es uno de los usos clásicos de la programación.
# En este ejemplo, crearemos un script que organiza archivos en una carpeta,
# distribuyéndolos en subcarpetas según su tipo. Por ejemplo, en la carpeta de "Descargas"
# tenemos una mezcla de imágenes, documentos PDF, vídeos, etc. Queremos que el script cree 
# subdirectorios como Imagenes, Documentos, Videos, Otros y mueva cada archivo al 
# correspondiente según su extensión. Este script se puede ejecutar manualmente o 
# programarse para que corra cada cierto tiempo.

#Pasos a seguir:
"""
- Definir categorías de extensiones (por ejemplo: imágenes = [".png", ".jpg", ".gif"], documentos = [".pdf", ".docx", ".txt"], etc.)
- Listar todos los archivos de la carpeta objetivo.
- Para cada archivo, determinar su extensión y, por tanto, su categoría.
- Crear la carpeta de categoría si no existe.
- Mover el archivo a esa carpeta. """

import os
from pathlib import Path

carpeta_objetivo = Path.home() / "Downloads"

categorias = {

    "Imagenes": [".png", ".jpg", ".jpeg", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Musica": [".mp3", ".wav"],
}

categorias_predeterminadas = ["Otros"]  # donde irá lo que no encaje en las anteriores
extension_a_categoria = {}

for categoria, exts in categorias.items(): #recorre las categorias y las extensiones

    for ext in exts:

        extension_a_categoria[ext.lower()] = categoria #diccionario que convierte la extension a la categoria

archivos = [f for f in carpeta_objetivo.iterdir() if f.is_file()] #lista de archivos en la carpeta objetivo

for archivo in archivos:

    ext = archivo.suffix.lower()

    categoria = extension_a_categoria.get(ext, "Otros")

    destino_dir = carpeta_objetivo / categoria

    destino_dir.mkdir(exist_ok=True)

    archivo.rename(destino_dir / archivo.name)

    print(f"Movido {archivo.name} a {categoria}/")