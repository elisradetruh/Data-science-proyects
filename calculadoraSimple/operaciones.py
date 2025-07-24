""" Crea un programa calculadora.py que:
Pide al usuario una operación (suma, resta, multiplicación, división) y dos números.
Ejecute la operación y muestre el resultado.
Debe repetirse hasta que el usuario escriba "salir" como operación."""

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    return a / b

# Pedir el primer número
resultado = float(input("Ingrese el primer número: "))

while True:
    operacion = input("Ingrese la operación (+, -, *, /) o salir: ")
    if operacion == "salir":
        print("Resultado final:", resultado)
        break
    siguiente = float(input("Ingrese el siguiente número: "))
    if operacion == "+":
        resultado = suma(resultado, siguiente)
    elif operacion == "-":
        resultado = resta(resultado, siguiente)
    elif operacion == "*":
        resultado = multiplicacion(resultado, siguiente)
    elif operacion == "/":
        resultado = division(resultado, siguiente)
    else:
        print("Operación no válida")
        continue
    print("Resultado actual:", resultado)