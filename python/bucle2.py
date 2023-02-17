for i in range(5, 50, 3):
    print(f"Valor de la variable {i}")

valido = False
email = input("Introduce tu email: ")

#Si agrego un 'continue' a un for sirve para saltar un recorrido e ir al siguiente
#El else en un for actua como un finally en un try catch
for i in range(len(email)):
    if email[i] == "@":
        valido = True

if valido:
    print("Email correcto")
else:
    print("Email incorrecto")