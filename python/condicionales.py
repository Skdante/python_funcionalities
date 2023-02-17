print("Salario deseado")
salario = int(input())

def evaluacion(nota):
    if 10000<nota<30000:
        valoracion = "se acepta"
    elif 30001<nota<35000:
        valoracion = "en revision"
    else:
        valoracion = "no lo aceptamos"

    return valoracion

print(evaluacion(salario))