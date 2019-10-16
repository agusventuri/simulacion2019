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
    
    def gettiempoFinAtencion(self):
        return self.tiempoFinAtencion

    def calcularProxFinAtencion(self):
        return 40


class Recepcion(Servidor):
    a = 3
    b = 7

    def calcularProxFinAtencion(self):
        r= round((self.a + random.random() * (self.b - self.a))*60,0)
        return r
        #return 90


class Balanza(Servidor):
    a = 5
    b = 7

    def calcularProxFinAtencion(self):
        # lo debe calcular segun atencion balanza
        r=round((self.a + random.random() * (self.b - self.a))*60,0)
        return r



class Darsena(Servidor):
    a = 15
    b = 20

    def __init__(self):
        Servidor.__init__(self)
        self.cantidadCamiones = 0
        self.cantRecalibrados = 0
        self.calibrando = False

    def getRecalibrados(self):
        return self.cantRecalibrados

    #falta implementarlo completo
    def obtenerTiempoRecalibrado(self):
        media = 10
        varianza = 1.2
        ri = random.random()
        res= round((media + (-2 * math.log(ri,math.e) * math.cos(2 * math.pi * ri + 1)) * math.sqrt(varianza)),0)
        return res

    def obtenerEvento(self):
        if (self.cantidadCamiones == 15):
            self.cantidadCamiones = 0
            self.cantRecalibrados += 1
            r = round((self.a + random.random() *(self.b - self.a) + self.obtenerTiempoRecalibrado())*60,0)
            self.tiempoFinAtencion = r
            self.calibrando = True
            self.ocupado = True

        if (self.calibrando):
            if (self.tiempoFinAtencion > 0):
                self.tiempoFinAtencion -= 1
                return None
            else:
                self.calibrando
                self.ocupado = False
                return None

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

    def calcularProxFinAtencion(self):
        # lo debe calcular segun atencion darsena
        self.cantidadCamiones += 1
        r = round((self.a + random.random() * (self.b - self.a))*60,0)
        return r

