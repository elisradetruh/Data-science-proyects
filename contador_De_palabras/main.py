import SepararPalabras as s
import Frecuencias as f
import contador as c

archivo = s.elegir_archivo()
try:
    with open(archivo, 'r', encoding='utf-8') as file:
        texto = file.read()
except FileNotFoundError:
    print(f"El archivo {archivo} no existe")
    exit(1)

palabras, total_palabras = s.separar_palabras(texto)
print(f"Total de palabras: {total_palabras}")

mas_comunes = f.frecuencias(palabras)
print("Palabras más frecuentes:")
for palabra, freq in mas_comunes:
    print(f"{palabra}: {freq}")

print(f"Total de palabras (por función contar_palabras: {c.contar_palabras(texto)}")