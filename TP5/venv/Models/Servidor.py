import random
import math
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
    a = 180
    b = 420

    def calcularProxFinAtencion(self):
        #return self.a + random.random() * (self.b - self.a)
        return 90


class Balanza(Servidor):
    a = 300
    b = 420
    def calcularProxFinAtencion(self):
        # lo debe calcular segun atencion balanza
        #return self.a + random.random() * (self.b - self.a)
        return 120


class Darsena(Servidor):
    cantidadCamiones = 0
    a = 900
    b = 1200

    #falta implementarlo completo
    def obtenerTiempoRecalibrado(self):
        media = 600
        varianza = 72
        ri = random.random()
        return media + (-2 * math.log(ri) * math.cos(2 * math.pi * ri + 1)) * math.sqrt(varianza)

    def calcularProxFinAtencion(self):
        # lo debe calcular segun atencion darsena
        if Darsena.cantidadCamiones == 15:
            Darsena.cantidadCamiones = 0
            #return self.a + random.random() *(self.b - self.a) + self.obtenerTiempoRecalibrado()
            return 140 + 50
        else:
            Darsena.cantidadCamiones += 1
            #return self.a + random.random() * (self.b - self.a)
            return 140
