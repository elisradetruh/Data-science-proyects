import re
import tkinter as tk
from tkinter import filedialog

def elegir_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo de texto",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    return archivo

def separar_palabras(texto):
    palabras = re.findall(r'\b\w+\b', texto.lower())
    total_palabras = len(palabras)
    return palabras, total_palabras

