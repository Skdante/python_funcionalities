class Empleado:

    def __init__(self, nombre, cargo, salario):
        self.nombre = nombre
        self.cargo = cargo
        self.salario = salario

    def __str__(self):
        return "{} que trabajo como {} tiene un salario de {} pesos".format(self.nombre, self.cargo, self.salario)


listaEmpleados = [
    Empleado("Samuel", "Director", 7500),
    Empleado("Pedro", "Presidente", 7000),
    Empleado("Antonio", "Administrativo", 1000),
    Empleado("Juan", "Vendedor", 2000)
]

'''
salarios_filtrados=filter(lambda empleado:empleado.salario>50000, listaEmpleados)

for empleado_salario in salarios_filtrados:
    print(empleado_salario)
'''

def calculo_comision(empleado):
    if empleado.salario > 3000:
        empleado.salario=empleado.salario*1.03
    return empleado

listaEmpleados=map(calculo_comision, listaEmpleados)

for empleado in listaEmpleados:
    print(empleado)

