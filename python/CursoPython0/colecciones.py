# Listas = Coleccion de elementos
colores = ["rojo", "amarillo", "verde"]
colores.append("naranja") # agregar otro elemento a la colección
colores.remove("amarillo") # remueve un elemento de la colección

# Tuplas = Coleccion de elementos que no se pueden modificar
tuplas_colores = ("rojo", "amarillo", "verde")
len(tuplas_colores) # Longitud de la tupla

# Conjuntos = Coleccion de elementos desordenados, es decir no hay indice para acceder a sus elementos.
conjunto_colores = {"rojo", "amarillo", "verde"}
conjunto_colores.add("negro")
conjunto_colores.remove("verde")

# Diccionarios = Coleccion de elementos que estan indexados pero no ordenados y se pueden modificar.
diccionario_colores = {"red":"rojo", "blue":"amarillo", "green":"verde"}
diccionario_colores["black"] = "negro" # Agregar otro elemento
diccionario_colores.pop("blue") # Quitamos un elemento
del(diccionario_colores["black"]) # Quitamos un elemento

