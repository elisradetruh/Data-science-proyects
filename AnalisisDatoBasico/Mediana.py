#generar una grafica de dispersion de las ventas vs años
#Usando el csv de sales_and_years calcular la Media de las ventas por año

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Agregar manejo de errores
try:
    df = pd.read_csv('sales_and_years.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo sales_and_years.csv")
    exit()

# Agregar validación de datos
if df.empty:
    print("Error: El archivo CSV está vacío")
    exit()

# Agregar más personalización visual
sns.set_style("whitegrid")  # Estilo más moderno

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
# Calcular y mostrar la media de las ventas
mediana_ventas = df['Ventas'].median() #median: mediana
print(f"La mediana de las ventas es: {mediana_ventas:.2f}")#:.2f: Formatea el número con 2 decimales

# Personalizar la gráfica
plt.title('Gráfica de Dispersión: Ventas vs Años', fontsize=14, fontweight='bold')
plt.text(0.5, 0.95, f'Mediana de las ventas: {mediana_ventas:.2f}', 
         transform=plt.gca().transAxes, ha='center', va='top', 
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
plt.xlabel('Años', fontsize=12)
plt.ylabel('Ventas', fontsize=12)
plt.grid(True, alpha=0.3)

# Rotar las etiquetas del eje X para mejor legibilidad
plt.xticks(rotation=45)

# Ajustar el layout para evitar cortes
plt.tight_layout()

# Mostrar la gráfica
plt.show()



