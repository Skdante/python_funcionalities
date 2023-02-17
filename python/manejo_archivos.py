from io import open
#Archivo de escritura
#archivo_texto = open("archivo_texto","w")
#frase="Estupendo dia para estudiar Python \n el miercoles"
#archivo_texto.write(frase)
#archivo_texto.close()s

#Archivo de lectura
#archivo_texto = open("archivo_texto", "r")
#print(archivo_texto.read())
#archivo_texto.seek(0)
#print(archivo_texto.read())
#archivo_texto.close()

#Archivo de lectura por lineas
#archivo_texto = open("archivo_texto", "r")
#lineas_texto = archivo_texto.readlines()
#archivo_texto.close()
#print(lineas_texto)

#Archivo de lectura para agregar mas texto a un archivo
#archivo_texto = open("archivo_texto", "a")
#archivo_texto.write("\n siempre es una buena ocasion para estudiar python")
#archivo_texto.close()

#Archivo de lectura y escritura
archivo_texto = open("archivo_texto", "r+")

try:
    lista_texto = archivo_texto.readlines()
    lista_texto[1] = " Esta linea ha sido incluida desde el exterior2 \n"
    archivo_texto.seek(0)
    archivo_texto.writelines(lista_texto)
finally:
    archivo_texto.close()