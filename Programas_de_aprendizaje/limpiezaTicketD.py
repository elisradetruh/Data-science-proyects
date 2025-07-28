import pandas as pd


df = pd.read_csv(r'C:\Users\israe\OneDrive\Documentos\Universidad\Python proyects\TicketD.csv', encoding='utf-8')

print("Columnas originales:", df.columns.tolist())

# Limpiar espacios
df.columns = df.columns.str.strip().str.upper()

print("Columnas limpias:", df.columns.tolist())

df['PRECIO'] = df['PRECIO'].astype(str).str.replace(r'[^\d.]', '', regex=True).astype(float) #Elimina cualquier carácter que no sea un número o un punto decimal
df['TOTAL'] = df['TOTAL'].astype(str).str.replace(r'[^\d.]', '', regex=True).astype(float)


df_limpio = df.groupby(['FOLIO', 'PRODUCTO']).agg({
    'UNIDADES': 'sum',
    'PRECIO': 'max'
}).reset_index()
#maximo y se suma
df_limpio['TOTAL'] = df_limpio['UNIDADES'] * df_limpio['PRECIO']

df_limpio['PRECIO'] = df_limpio['PRECIO'].astype(int)
df_limpio['TOTAL'] = df_limpio['TOTAL'].astype(int)

df_limpio.to_csv('TicketDLimpio.csv', index=False)
print("Listo: archivo_limpio.csv")