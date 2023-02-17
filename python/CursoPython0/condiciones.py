colores = ["rojo", "amarillo", "verde"]
a = 8
b = 4
c = 2
d = 6

# if, elif, else
if(a > b):
    print("a es mayor que b")

if(a > c) and (b > d):
    print("La primera expresion es correcta")
elif(a == b):
    print("Esta expression es correcta")
else:
    print("La primera expresion no es correcta")

# For
for color in colores:
    print(color)