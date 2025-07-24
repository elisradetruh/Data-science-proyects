from collections import Counter

def frecuencias(palabras):
    contador = Counter(palabras)
    return contador.most_common(10)