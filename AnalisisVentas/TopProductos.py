import pandas as pd
import Analisis as A
import matplotlib.pyplot as plt

top5 = A.ventas_prod.nlargest(5, 'Ingreso')

plt.figure(figsize=(6,4))

plt.bar(top5.index, top5['Ingreso'])

plt.title("Top 5 Productos por Ingresos")

plt.ylabel("Ingresos (€)")

plt.xlabel("Producto")

plt.tight_layout()

plt.show()