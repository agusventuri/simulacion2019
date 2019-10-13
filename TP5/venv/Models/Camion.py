import random

class Camion:
    # variables comunes a todos los objetos Camion
    cantidadColaBalanza = [0] * 30
    cantidadColaRecepcion = [0] * 30
    cantidadColaDarsenas = [0] * 30
    cantidadColaTerminados = [0] * 30
    cantidadTotal = 0

    def __init__(self, dia):
        self.cola = 1
        self.dia = dia
        self.posicion = Camion.cantidadColaRecepcion[dia - 1] + 1
        Camion.cantidadColaRecepcion[dia - 1] += 1
        self.nroCamion = Camion.cantidadTotal + 1
        Camion.cantidadTotal += 1
        self.propio = True
        if (random.random() > 0.35):
            self.propio = False

    def getPropio(self):
        return self.propio

    def avanzar(self):
        if(self.posicion - 1 != 0):
            self.posicion -= 1
        else:
            if(self.cola == 1 and self.propio == False):
                self.cola = 2
                self.posicion = Camion.cantidadColaBalanza[self.dia - 1] + 1
                Camion.cantidadColaRecepcion[self.dia - 1] -= 1
                Camion.cantidadColaBalanza[self.dia - 1] += 1
            elif(self.cola == 1 and self.propio == True):
                self.cola = 3
                self.posicion = Camion.cantidadColaDarsenas[self.dia - 1] + 1
                Camion.cantidadColaRecepcion[self.dia - 1] -= 1
                Camion.cantidadColaDarsenas[self.dia - 1] += 1
            elif(self.cola == 2):
                self.cola = 3
                self.posicion = Camion.cantidadColaDarsenas[self.dia - 1] + 1
                Camion.cantidadColaBalanza[self.dia - 1] -= 1
                Camion.cantidadColaDarsenas[self.dia - 1] += 1
            else:
                self.cola = 4
                self.posicion = Camion.cantidadColaTerminados[self.dia - 1] + 1
                Camion.cantidadColaDarsenas[self.dia - 1] -= 1
                Camion.cantidadColaTerminados[self.dia - 1] += 1
        return True

c1 = Camion(1)
c2 = Camion(1)
c3 = Camion(1)
c4 = Camion(1)
c5 = Camion(1)
c6 = Camion(1)
c1.avanzar()
c2.avanzar()
c3.avanzar()
c4.avanzar()
c5.avanzar()
c6.avanzar()
c2.avanzar()

print("camion 1")
print("pos" + str(c1.posicion))
print("cola" + str(c1.cola))
print("camion 2")
print("pos" + str(c2.posicion))
print("cola" + str(c2.cola))
print("camion 3")
print("pos" + str(c3.posicion))
print("cola" + str(c3.cola))
print("camion 4")
print("pos" + str(c4.posicion))
print("cola" + str(c4.cola))
print("camion 5")
print("pos" + str(c5.posicion))
print("cola" + str(c5.cola))
print("camion 6")
print("pos" + str(c6.posicion))
print("cola" + str(c6.cola))

print(Camion.cantidadColaRecepcion)