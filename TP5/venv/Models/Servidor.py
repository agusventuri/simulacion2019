import random
import math
from abc import ABCMeta, abstractmethod
import datetime


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

    def getNroCliente(self):
        if (self.camion is None):
            return "----"
        return self.camion.getnroCamion()

    def getEstado(self):
        if self.getOcupado():
            return "Ocupado"
        return "Libre"

    def getOcupado(self):
        return self.ocupado
    
    def gettiempoFinAtencion(self):
        return self.convert_timedelta(self.tiempoFinAtencion)

    def gettiempoFinAtencionSegundos(self):
        return self.tiempoFinAtencion

    def calcularProxFinAtencion(self):
        return 40

    def convert_timedelta(self, seconds):
        duration = datetime.timedelta(seconds=seconds)
        days, seconds = duration.days, duration.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = (seconds % 60)
        return days, hours, minutes, secs


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

    def getNroCliente(self):
        if (self.calibrando or self.camion is None):
            return "----"
        return self.camion.getnroCamion()

    #falta implementarlo completo
    def obtenerTiempoRecalibrado(self):
        media = 10
        varianza = 1.2
        ri = random.random()
        res= round((media + (-2 * math.log(ri,math.e) * math.cos(2 * math.pi * ri + 1)) * math.sqrt(varianza)) * 60,0)
        return res

    def getCamionesAtendidos(self):
        if self.cantidadCamiones == 14 and self.calibrando:
            return "----"
        return self.cantidadCamiones + 1

    def getEstado(self):
        if self.calibrando:
            return "Calibrando"
        if self.getOcupado():
            return "Ocupado"
        return "Libre"

    def obtenerEvento(self):
        if (self.cantidadCamiones == 14 and not self.calibrando):
            self.cantRecalibrados += 1
            r = self.obtenerTiempoRecalibrado()
            self.tiempoFinAtencion = r
            self.calibrando = True
            self.ocupado = True
            #empieza calibrar
            return True

        if (self.calibrando):
            if (self.tiempoFinAtencion > 0):
                self.tiempoFinAtencion -= 1
                #esta calibrando
                return None
            else:
                self.cantidadCamiones = 0
                self.calibrando = False
                self.ocupado = False
                #termino calibrado
                return False

        if (self.camion is not None):
            if (self.tiempoFinAtencion > 0):
                self.tiempoFinAtencion -= 1
                #esta atendiendo
                return None
            else:
                c = self.camion
                self.camion = None
                self.ocupado = False
                self.cantidadCamiones += 1
                #termino atender
                return c
        return None

    def calcularProxFinAtencion(self):
        # lo debe calcular segun atencion darsena
        r = round((self.a + random.random() * (self.b - self.a))*60,0)
        return r

    def getCalibrando(self):
        if (self.cantidadCamiones == 15 or self.calibrando):
            return True
        return self.calibrando;
