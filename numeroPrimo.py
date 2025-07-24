#TODO determinar si un número es primo

def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            print(f"El numero {n} no es primo porque es divisible por {i}")
            return False
    print(f"El numero {n} es primo")
    return True

numero = int(input("Ingresa tu numero para ver si es primo: "))
es_primo(numero)