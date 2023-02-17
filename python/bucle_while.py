edad = int(input("Introduce la edad: "))

while edad<5 or edad>100:
    print("Has introducido una edad incorrecta")
    edad = int(input("Introduce tu edad por favor: "))

print("Gracias por colaborar, puedes pasar")
print(f"Edad del aspirante: {edad} años")