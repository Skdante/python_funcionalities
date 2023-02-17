miLista = ["Juan", "Maria", "Pepe", "Antonio"]
miLista.append("Sandra")
miLista.insert(2,"Sandra")
miLista.extend(["Juan", "Maria", "Pepe", "Antonio"])
print(miLista[:])
print(miLista[2])
print(miLista[0:3])
print(miLista[1:3])
print(miLista.index("Antonio"))
#Busca si existe el elemento Pepe en la lista
print("Pepe" in miLista)
print("Pepes" in miLista)
print("Pepes" in miLista)   
#Elimina elementos
#miLista.remove(2)
miLista.pop()