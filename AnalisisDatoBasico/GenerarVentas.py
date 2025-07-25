import random as rd
import pandas as pd

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
sales = [rd.randint(100, 10000) for _ in range(len(years))]
"""
Otra forma de hacerlo es con
#Generacion de la columna Ventas con su encabezado
sales_column = pd.DataFrame(sales, columns=['Ventas'])

#Generacion de la columna Años con su encabezado
years_column = pd.DataFrame(years, columns=['Años'])
"""
# Crear el DataFrame directamente
sales_and_years = pd.DataFrame({
    'Años': years,
    'Ventas': sales
})

sales_and_years.to_csv('sales_and_years.csv', index=False)
print(sales_and_years.head())









