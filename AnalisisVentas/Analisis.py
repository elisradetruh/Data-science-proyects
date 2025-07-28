#TODO: Calcular total de ventas por mes ,Determinar el producto mas vendido y 
# con mayor ingresos,Graficar ventas por mes , Graficar top 5 productos por ingresos

import pandas as pd

df = pd.read_csv('datos_ventas.csv')
df['Fecha'] = pd.to_datetime(df['Fecha']) #v. Asegúrate también de que los tipos son correctos: cantidad y precio deben ser numéricos (ints/floats).

df['Mes'] = df['Fecha'].dt.to_period('M')
ventas_por_mes = df.groupby('Mes').apply(lambda x: (x['Cantidad Vendida'] * x['Precio']).sum())
ventas_por_mes = ventas_por_mes.sort_index()

df['Ingreso'] = df['Cantidad Vendida'] * df['Precio']

ventas_prod = df.groupby('Producto').agg({
    'Cantidad Vendida': 'sum',
    'Ingreso': 'sum'
})

mas_vendido = ventas_prod['Cantidad Vendida'].idxmax()
mas_ingresos = ventas_prod['Ingreso'].idxmax()

print(f"El producto con mayor ingresos es: {mas_ingresos} (Total: ${ventas_prod.loc[mas_ingresos, 'Ingreso']:,.2f})")
print(f"El producto más vendido es: {mas_vendido} (Total: {ventas_prod.loc[mas_vendido, 'Cantidad Vendida']:,} unidades)")

print("\n" + "="*50)
print("VENTAS POR MES:")
print("="*50)
for mes, ventas in ventas_por_mes.items():
    print(f"{mes}: ${ventas:,.2f}")

print("\n" + "="*50)
print("TOP 5 PRODUCTOS POR INGRESOS:")
print("="*50)
top_5_ingresos = ventas_prod.sort_values('Ingreso', ascending=False).head(5)
for idx, (producto, datos) in enumerate(top_5_ingresos.iterrows(), 1):
    print(f"{idx}. {producto}: ${datos['Ingreso']:,.2f}")

print("\n" + "="*50)
print("TOP 5 PRODUCTOS POR CANTIDAD VENDIDA:")
print("="*50)
top_5_cantidad = ventas_prod.sort_values('Cantidad Vendida', ascending=False).head(5)
for idx, (producto, datos) in enumerate(top_5_cantidad.iterrows(), 1):
    print(f"{idx}. {producto}: {datos['Cantidad Vendida']:,} unidades")








