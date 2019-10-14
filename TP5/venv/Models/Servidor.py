import random
from abc import ABCMeta, abstractmethod


class Servidor:

    def __init__(self):
        self.camion = None
        self.tiempoFinAtencion = 0
        self.ocupado = False

    def obtenerEvento(self):
        if (self.camion is not None):
            if (self.tiempoFinAtencion > 0):
                self.tiempoFinAtencion -= 1
                return None
            else:
                c = self.camion
                self.camion = None
                self.ocupado = False
                return c
        return None

    def recibirCamion(self, camion):
        self.camion = camion
        self.tiempoFinAtencion = self.calcularProxFinAtencion()
        self.ocupado = True

    def getOcupado(self):
        return self.ocupado

    def calcularProxFinAtencion(self):
        return 40


class Recepcion(Servidor):

    def calcularProxFinAtencion(self):
        return random.randrange(90, 420)


class Balanza(Servidor):

    def calcularProxFinAtencion(self):
        # lo debe calcular segun atencion balanza
        return 40


class Darsena(Servidor):

    def calcularProxFinAtencion(self):
        # lo debe calcular segun atencion darsena
        return 40