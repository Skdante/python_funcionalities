import re
lista_nombres = ['Ana Gómez', 'Maria Martin', 'Sandra Lopez', 'Santiago Martin', 'Carlos Sonoto']
'''
for nombre in lista_nombres:
    if re.findall('^San', nombre):
        print(nombre)
'''
for nombre in lista_nombres:
    if re.findall('S[ao]n', nombre):
        print(nombre)

# El caracter (^) sirve para que después de eso la apalabra que se agregue debe de ir al inicio de lo que buscamos
# El caracter ($) sirve para que al final de la palabra que se agregue debe de ir al final de lo que buscamos
# El caracter ([]) sirve para indicar que la letra que sigue puede tener mas de una opción