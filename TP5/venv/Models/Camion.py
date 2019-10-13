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

    def avanzarPosicion(self):
        self.posicion -= 1
        return True

    def avanzarADos(self):
        self.cola = 2
        self.posicion = Camion.cantidadColaBalanza[self.dia - 1] + 1
        Camion.cantidadColaRecepcion[self.dia - 1] -= 1
        Camion.cantidadColaBalanza[self.dia - 1] += 1

    def avanzarATres(self):
        if(self.cola == 2):
            Camion.cantidadColaBalanza[self.dia - 1] -= 1
        else:
            Camion.cantidadColaRecepcion[self.dia - 1] -= 1
        self.cola = 3
        self.posicion = Camion.cantidadColaDarsenas[self.dia - 1] + 1
        Camion.cantidadColaDarsenas[self.dia - 1] += 1

    def salirDelPredio(self):
        self.cola = 4
        self.posicion = Camion.cantidadColaTerminados[self.dia - 1] + 1
        Camion.cantidadColaDarsenas[self.dia - 1] -= 1
        Camion.cantidadColaTerminados[self.dia - 1] += 1
