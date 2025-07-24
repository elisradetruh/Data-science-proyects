#FizzBuzz es un juego de niños que consiste en decir los numeros del 1 al 50 y reemplazar los numeros que son multiplos de 3 por fizz y los que son multiplos de 5 por buzz y los que son multiplos de 3 y 5 por fizzbuzz

for i in range(1, 51): #Cuando un numero es multiplo de 3 y 5 es fizz buzz para eso es el % para los multiplos
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz") #Cuando un numero es multiplo de 3 es fizz
    elif i % 5 == 0:
        print("Buzz") #Cuando un numero es multiplo de 5 es buzz
    else:
        print(i)