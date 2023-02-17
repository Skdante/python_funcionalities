def compruebaMail(mailUsuario):
    """
        La funcion compurba mail, evalue un mail recibido en busca de la arroba. 
    
        >>> compruebaMail('samuel123@gmail.com')
        True

        >>> compruebaMail('samuel123gmail.com')
        False

        >>> compruebaMail('samuel123gmail.com@')
        False

        >>> compruebaMail('samuel123@gmail.com@')
        False
    """
    arroba=mailUsuario.count('@')
    if (arroba!=1 or mailUsuario.rfind('@')==(len(mailUsuario)-1) or mailUsuario.find('@')==0):
        return False
    else:
        return True


import doctest
doctest.testmod()