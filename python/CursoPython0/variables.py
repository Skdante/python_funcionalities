# Variables
texto = "Hola Mundo"
numero_entero = 10
numero_decimal = 3.7
numero_entero2 = 3
resultado = numero_entero / numero_entero2 

# Imprimir los valores
print(texto)
print("El resultado es {a:1.2f}".format(a=resultado))

# Podemos saber cual es el tipo de la variable con el metodo type
print(type(texto))
print(type(numero_decimal))

# Conversion de datos
numero_texto = str(numero_decimal)
texto_numero = float(numero_texto)