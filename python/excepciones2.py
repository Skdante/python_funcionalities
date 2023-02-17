def evalueEdad(edad):
    if edad<0:
        raise TypeError("No se permiten edades negativas")
    else:
        return "Adelante"