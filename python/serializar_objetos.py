import pickle

class Vehiculos():
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.enmarcha = False
        self.frena = False
        self.acelera = False

    def arrancar(self):
        self.enmarcha = True

    def acelerar(self):
        self.acelera = True

    def frenar(self):
        self.frena = True

    def estado(self):
        print("Marca: ", self.marca, "\nModelo: ", self.modelo, "\nEn Marcha", self.enmarcha)

coche1 = Vehiculos("Mazda", "M5")
coche2 = Vehiculos("Seat", "Leon")
coche3 = Vehiculos("Renault", "Megane")

coches = [coche1, coche2, coche3]
#fichero = open("losCoches", "wb")
#pickle.dump(coches, fichero)
#fichero.close()
#del(fichero)

ficheroApertura = open("losCoches", "rb")
misCoches = pickle.load(ficheroApertura)
ficheroApertura.close()

for c in misCoches:
    print(c.estado())