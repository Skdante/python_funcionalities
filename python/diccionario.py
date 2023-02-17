midiccionario = {"Pais": "México", "Francia":"Brasil", "Estado": "Nuevo Leon", "Apodaca": "Hola"}
print(midiccionario)
print(midiccionario["Pais"])
#agregar un elemento del diccionario
midiccionario["Italia"] = "Paris"
print(midiccionario)
#eliminar un elemento dentro del diccionario
del midiccionario["Francia"]
print(midiccionario)
print(midiccionario.keys())
print(midiccionario.values())