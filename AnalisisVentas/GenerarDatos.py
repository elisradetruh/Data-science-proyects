import pandas as pd
import random as rd

"""Generar columnas como fecha, producto, cantidad vendida, precio """

# Diccionario con productos, precios y rangos de cantidad
productos = {
    'Shampoo': {'precio': 100, 'cantidad_min': 100, 'cantidad_max': 1000},
    'Jabon': {'precio': 100, 'cantidad_min': 100, 'cantidad_max': 1000},
    'Desodorante': {'precio': 100, 'cantidad_min': 100, 'cantidad_max': 1000},
    'Cepillo': {'precio': 50, 'cantidad_min': 50, 'cantidad_max': 300},
    'Cremas': {'precio': 120, 'cantidad_min': 80, 'cantidad_max': 400},
    'Condones': {'precio': 170, 'cantidad_min': 500, 'cantidad_max': 1000},
    'Toallas Femeninas': {'precio': 70, 'cantidad_min': 100, 'cantidad_max': 500},
    'Pasta Dental': {'precio': 45, 'cantidad_min': 80, 'cantidad_max': 400},
    'Enjuague Bucal': {'precio': 85, 'cantidad_min': 50, 'cantidad_max': 200},
    'Papel Higienico': {'precio': 35, 'cantidad_min': 200, 'cantidad_max': 800},
    'Toallas de Papel': {'precio': 25, 'cantidad_min': 150, 'cantidad_max': 600},
    'Servilletas': {'precio': 20, 'cantidad_min': 100, 'cantidad_max': 500},
    'Detergente': {'precio': 75, 'cantidad_min': 50, 'cantidad_max': 300},
    'Suavizante': {'precio': 65, 'cantidad_min': 40, 'cantidad_max': 200},
    'Cloro': {'precio': 40, 'cantidad_min': 30, 'cantidad_max': 150},
    'Limpiavidrios': {'precio': 55, 'cantidad_min': 20, 'cantidad_max': 100},
    'Escoba': {'precio': 120, 'cantidad_min': 10, 'cantidad_max': 50},
    'Trapeador': {'precio': 95, 'cantidad_min': 15, 'cantidad_max': 60},
    'Cubeta': {'precio': 150, 'cantidad_min': 5, 'cantidad_max': 25},
    'Guantes de Limpieza': {'precio': 35, 'cantidad_min': 20, 'cantidad_max': 80},
    'Esponjas': {'precio': 15, 'cantidad_min': 50, 'cantidad_max': 200},
    'Desinfectante': {'precio': 45, 'cantidad_min': 30, 'cantidad_max': 120},
    'Ambientador': {'precio': 65, 'cantidad_min': 25, 'cantidad_max': 100},
    'Velas': {'precio': 30, 'cantidad_min': 20, 'cantidad_max': 80},
    'Fosforos': {'precio': 8, 'cantidad_min': 30, 'cantidad_max': 120},
    'Baterias': {'precio': 25, 'cantidad_min': 40, 'cantidad_max': 150},
    'Focos': {'precio': 35, 'cantidad_min': 30, 'cantidad_max': 100},
    'Cables USB': {'precio': 45, 'cantidad_min': 15, 'cantidad_max': 60},
    'Cargadores': {'precio': 85, 'cantidad_min': 10, 'cantidad_max': 40},
    'Protectores Solares': {'precio': 95, 'cantidad_min': 20, 'cantidad_max': 80},
    'Repelente de Insectos': {'precio': 55, 'cantidad_min': 15, 'cantidad_max': 60},
    'Vitaminas': {'precio': 125, 'cantidad_min': 30, 'cantidad_max': 100},
    'Aspirinas': {'precio': 35, 'cantidad_min': 50, 'cantidad_max': 200},
    'Curitas': {'precio': 25, 'cantidad_min': 40, 'cantidad_max': 150},
    'Algodon': {'precio': 20, 'cantidad_min': 30, 'cantidad_max': 120},
    'Alcohol': {'precio': 30, 'cantidad_min': 25, 'cantidad_max': 100},
    'Perfume': {'precio': 180, 'cantidad_min': 10, 'cantidad_max': 40},
    'Maquillaje': {'precio': 95, 'cantidad_min': 15, 'cantidad_max': 60},
    'Brochas': {'precio': 45, 'cantidad_min': 20, 'cantidad_max': 80},
    'Espejos': {'precio': 75, 'cantidad_min': 10, 'cantidad_max': 40},
    'Peines': {'precio': 35, 'cantidad_min': 25, 'cantidad_max': 100},
    'Cortauñas': {'precio': 25, 'cantidad_min': 30, 'cantidad_max': 120},
    'Tijeras': {'precio': 55, 'cantidad_min': 15, 'cantidad_max': 50},
    'Cinta Adhesiva': {'precio': 20, 'cantidad_min': 40, 'cantidad_max': 150},
    'Lapices': {'precio': 15, 'cantidad_min': 100, 'cantidad_max': 400},
    'Cuadernos': {'precio': 45, 'cantidad_min': 50, 'cantidad_max': 200},
    'Mochilas': {'precio': 250, 'cantidad_min': 5, 'cantidad_max': 20},
    'Paraguas': {'precio': 120, 'cantidad_min': 10, 'cantidad_max': 40},
    'Sombreros': {'precio': 85, 'cantidad_min': 15, 'cantidad_max': 60},
    'Bufandas': {'precio': 65, 'cantidad_min': 20, 'cantidad_max': 80},
    'Guantes': {'precio': 55, 'cantidad_min': 25, 'cantidad_max': 100},
    'Calcetines': {'precio': 35, 'cantidad_min': 80, 'cantidad_max': 300}
}

# Generar fechas
fecha = pd.date_range(start='2023-01-01', end='2025-06-30', freq='D')

# Listas para almacenar los datos
fechas_list = []
productos_list = []
cantidades_list = []
precios_list = []

# Generar datos para cada fecha
for fecha_actual in fecha:
    # Determinar cuántos productos se venderán en este día (entre 2 y 25 productos)
    num_productos_dia = rd.randint(2, 25)
    
    # Seleccionar productos aleatorios para este día (sin repetir)
    productos_del_dia = rd.sample(list(productos.keys()), num_productos_dia)
    
    # Generar datos para cada producto vendido en este día
    for producto_seleccionado in productos_del_dia:
        # Obtener información del producto desde el diccionario
        info_producto = productos[producto_seleccionado]
        cantidad_vendida = rd.randint(info_producto['cantidad_min'], info_producto['cantidad_max'])
        precio = info_producto['precio']
        
        # Agregar datos a las listas
        fechas_list.append(fecha_actual)
        productos_list.append(producto_seleccionado)
        cantidades_list.append(cantidad_vendida)
        precios_list.append(precio)

# Crear el DataFrame
df = pd.DataFrame({
    'Fecha': fechas_list,
    'Producto': productos_list,
    'Cantidad Vendida': cantidades_list,
    'Precio': precios_list
})

# Guardar el archivo CSV
df.to_csv('datos_ventas.csv', index=False)
print("Datos generados exitosamente!")
print(f"Total de registros: {len(df)}")
print(f"Total de días: {len(fecha)}")
print(f"Promedio de productos por día: {len(df)/len(fecha):.1f}")
print("\nPrimeras 15 filas:")
print(df.head(15))





