import re

nombre1="Lara Lopez"
nombre2="Antonio Gómez"
nombre3="Jara Lopez"

if re.match(".ara", nombre1, re.IGNORECASE):
    print("Hemos encontrado el nombre")
else:
    print("No lo hemos encontrado")


if re.search("ope", nombre1, re.IGNORECASE):
    print("Hemos encontrado el nombre")
else:
    print("No lo hemos encontrado")

# Cuando ponemos el (.) significa que esa letra es un comodin
# La funcion match revisa al principio de la cadena de texto
# La funcion search revisa en cualquier punto de texto