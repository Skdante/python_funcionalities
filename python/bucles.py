miEmail = input("Introduce tu email: ")
email = False

for i in [2,3,4]:
    print(i, end=" ")

for i in miEmail:
    if i == "@":
        email = True

if email:
    print("Email es correcto")
else:
    print("Email es incorrecto")