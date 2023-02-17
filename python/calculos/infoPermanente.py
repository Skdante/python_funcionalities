import pickle

class Persona:

    def __init__(self, nombre, genero, edad):
        self.nombre = nombre
        self.genero = genero
        self.edad = edad
        print("Se ha creado una persona nueva con el nombre ", self.nombre)

    def __str__(self):
        return "{} {} {}".format(self.nombre, self.genero, self.edad)

class ListaPersonas:
    
    personas = []

    def __init__(self):
        listaDePersonas = open("ficheroexterno", "ab+")
        listaDePersonas.seek(0)

        try:
            self.personas = pickle.load(listaDePersonas)
            print("Se cargaron {} personas personas del fichero externo".format(len(self.personas)))
        except:
            print("El fichero esta vacio")
        finally:
            listaDePersonas.close()
            del(listaDePersonas)

    def agregarpersonas(self, p):
        self.personas.append(p)
        self.guardarPersonasEnFicheroExterno()
    
    def mostrarpersonas(self):
        for c in self.personas:
            print(c)

    def guardarPersonasEnFicheroExterno(self):
        listaPersonas = open("ficheroexterno", "wb")
        pickle.dump(self.personas, listaPersonas)
        listaPersonas.close()
        del(listaPersonas)

    def mostrarInfoFicheroExterno(self):
        print("La informacion del ficher externo es la siguiente:")
        for p in self.personas:
            print(p)

miLista = ListaPersonas()
persona = Persona("Sandra", "Femenino", 29)
miLista.agregarpersonas(persona)
miLista.mostrarInfoFicheroExterno()