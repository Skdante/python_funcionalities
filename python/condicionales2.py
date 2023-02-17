print("Progarama de becas año 2020")
distancia_escuela = int(input("Introduce la distancia de la escuela en km:"))
print(distancia_escuela)

numero_hermanos = int(input("Introduce el n de hermanos en el cuarto:"))
print(numero_hermanos)

salario_familiar = int(input("Introduce salario anual bruto:"))
print(salario_familiar)

if distancia_escuela > 40 and numero_hermanos > 2 and salario_familiar <= 20000:
    print("Tienes derecho a beca")
else: 
    print("No tienes derecho a beca")