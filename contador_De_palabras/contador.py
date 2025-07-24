
import re
#TODO Dado un archivo de texto, contar el número de palabras que contiene
"""
def contar_palabras(archivo):
    with open(archivo, 'r') as file: #r es para modo lectura, w es para modo escritura, a es para modo append
        contenido = file.read()
        palabras = contenido.split()
        return len(palabras)

print("Las palabras en total fueron: ", contar_palabras("archivopalabras.txt"))
"""
def contar_palabras(texto):
    palabras = texto.split()
    return len(palabras)
