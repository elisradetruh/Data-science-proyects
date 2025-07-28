import matplotlib.pyplot as plt
import pandas as pd
import Analisis as A

A.ventas_por_mes.index = A.ventas_por_mes.index.astype(str) # Convertir el índice a string para que se pueda graficar

plt.figure(figsize=(10, 6))
plt.plot(A.ventas_por_mes.index, A.ventas_por_mes.values, marker='o', linestyle='-', color='b')
plt.title('Ventas por Mes')
plt.xlabel('Mes')
plt.ylabel('Ventas (USD)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafica_ventas_por_mes.png')
plt.show()

""" 📊 Explicación de los valores del eje Y:
Escala de valores:
3.00e6 = $3,000,000 (3 millones de dólares)
3.25e6 = $3,250,000 (3.25 millones de dólares)
3.50e6 = $3,500,000 (3.5 millones de dólares)
4.00e6 = $4,000,000 (4 millones de dólares)
4.50e6 = $4,500,000 (4.5 millones de dólares)
5.00e6 = $5,000,000 (5 millones de dólares)"""