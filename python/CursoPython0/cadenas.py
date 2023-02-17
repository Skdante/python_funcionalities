cadena_nombre = "Samuel"
cadena_apellido = "Rodriguez"
cadena_1 = "Hola"
cadena_2 = "Mundo"
cadena_completa = cadena_1 + " " + cadena_2

print(cadena_completa[3])
print(cadena_completa[-3]) # Recorrido inverso
print(cadena_completa[3:7])
print(len(cadena_completa)) # Tamaño de la cadena
print(cadena_completa.upper()) # Todo a Mayusculas
print(cadena_completa.lower()) # Todo a Minusculas
print(cadena_completa.split(' ')) # Separacion por este caso con espacio
print("Buenos dias {} tu apellido es {}".format(cadena_nombre, cadena_apellido))
print("Buenos dias {a} tu apellido es {b}".format(b=cadena_nombre, a=cadena_apellido))
print(f"Buenos dias {cadena_nombre} tu apellido es {cadena_apellido}")

input("Introdce un numero")
entrada = input()
print("tu numero es " + entrada)