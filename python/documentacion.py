import funciones_matematicas

class Areas:    
    ''' 
        Clase para las figuras geometricas
    '''

    def areaCuadrado(lado):
        ''' 
        Comentario multilinea de la funcion areaCuadrado
        '''
        return "El área del cuadrado es " + str(lado*lado)

    def areaTriangulo(base, altura):
        ''' 
            Comentario multilinea del area triangulo
        '''
        return "El area del triangulo es " + str((base * altura) / 2)

# print(Areas.areaCuadrado.__doc__)
# help(Areas.areaCuadrado)
# help(Areas)
help(funciones_matematicas)