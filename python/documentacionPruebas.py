def areaTriangulo(base, altura):
    '''
        Metodo para el area del triangulo
        >>> areaTriangulo(3,6)
        9.0

        >>> areaTriangulo(4,8)
        16.0
    '''
    return (base * altura) / 2

#print(areaTriangulo(2,4))
import doctest
doctest.testmod()