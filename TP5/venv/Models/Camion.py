import random

class Camion:
    # variables comunes a todos los objetos Camion
    cantidadTotal = 0

    def __init__(self, horaEntrada, camionPropio):
        self.nroCamion = Camion.cantidadTotal + 1
        Camion.cantidadTotal += 1
        self.propio = camionPropio
        self.horaEntrada = horaEntrada

    def getPropio(self):
        return self.propio

    def getnroCamion(self):
        if self.nroCamion is not None:
            return self.nroCamion
        else:
            return ""

    def setHoraSalida(self, hora):
        self.horaSalida = hora

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
