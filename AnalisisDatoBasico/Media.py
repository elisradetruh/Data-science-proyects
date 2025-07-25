#Usando el csv de sales_and_years calcular la Media de las ventas por año

import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos del CSV
df = pd.read_csv('sales_and_years.csv')

# Crear la gráfica de dispersión
plt.figure(figsize=(10, 6))
#: Crea una nueva figura (ventana de gráfica)
#Define el tamaño de la gráfica (10 pulgadas de ancho, 6 de alto)
plt.scatter(df['Años'], df['Ventas'], alpha=0.7, s=100, c='blue', edgecolors='black')
"""
#Crea un gráfico de dispersión (scatter plot)
#df['Años']: Columna de años
#df['Ventas']: Columna de ventas
#alpha=0.7: Transparencia de los puntos (0.0 = completamente transparente, 1.0 = completamente opaco)
#s=100: Tamaño de los puntos
#c='blue': Color de los puntos
"""

# Personalizar la gráfica
plt.title('Gráfica de Dispersión: Ventas vs Años', fontsize=14, fontweight='bold')
plt.xlabel('Años', fontsize=12)
plt.ylabel('Ventas', fontsize=12)
plt.grid(True, alpha=0.3)

# Rotar las etiquetas del eje X para mejor legibilidad
plt.xticks(rotation=45)

# Ajustar el layout para evitar cortes
plt.tight_layout()

# Mostrar la gráfica
plt.show()

# Calcular y mostrar la media de las ventas
media_ventas = df['Ventas'].mean()
print(f"La media de las ventas es: {media_ventas:.2f}")#:.2f: Formatea el número con 2 decimales

# Calcular y mostrar la desviación estándar de las ventas
desviacion_estandar = df['Ventas'].std()
print(f"La desviación estándar de las ventas es: {desviacion_estandar:.2f}")

# Mostrar estadísticas descriptivas completas
print("\nEstadísticas descriptivas completas:")
print(df['Ventas'].describe())

