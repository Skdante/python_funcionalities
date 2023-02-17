#De tupla a lista
miTupla = ("Juan", 13, 1, 1995)
print(miTupla[:])
print(list(miTupla[:]))

#De lista a tupla
miLista = ["Juan", 13, 1, 1995, 13]
print(miLista[:])
print(tuple(miLista[:]))
#Revisa cuantos num 13 hay en una tupla
print(tuple(miLista[:]).count(13))
#Revisa cuantos elementos hay en una tupla
print(len(tuple(miLista[:])))
#Asignacion de tupla a variables
mivariable = ("Juan", 13, 1, 1995)
nombre, dia, mes, agno=mivariable
print(agno)