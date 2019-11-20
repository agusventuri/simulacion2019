from Models.Distribucion import IDistribucion
from datetime import datetime
from datetime import timedelta
from collections import deque
import random
import copy


class Secador():

    def __init__(self, distribucionAtencion1, distribucionAtencion2, nombre):
        self.distribucionAtencion1 = distribucionAtencion1
        self.distribucionAtencion2 = distribucionAtencion2
        self.cliente1 = None
        self.cliente2 = None
        self.nombre = nombre
        self.estado = "Libre"
        self.cantidadAtendidos = 0
        self.proximoFinAtencion1 = datetime(100, 1, 1, 0, 0, 0)
        self.proximoFinAtencion2 = datetime(100, 1, 1, 0, 0, 0)

    def calcularFinAtencion(self, hora, primero):
        if primero:
            demora = round(self.distribucionAtencion1.generar(100) * 60, 0)
        else:
            demora = round(self.distribucionAtencion2.generar(100) * 60, 0)
        return hora + timedelta(seconds=demora)

    def llegadaDeCliente(self, hora, cliente):
        if (self.cliente1 is None):
            self.cliente1 = cliente
            self.cliente1.comenzarAtencion(hora, self.nombre)
            self.estado = "Atendiendo a " + str(self.cliente1.numero)
            self.proximoFinAtencion1 = self.calcularFinAtencion(hora, True)
        else:
            self.cliente2 = cliente
            self.cliente2.comenzarAtencion(hora, self.nombre)
            self.estado = "Atendiendo a " + str(self.cliente2.numero)
            self.proximoFinAtencion2 = self.calcularFinAtencion(hora, False)

        if (self.cliente1 is not None and self.cliente2 is not None):
            self.estado = "Atendiendo a " + str(self.cliente1.numero) + " y a " + str(self.cliente2.numero)

    def getProximoFinAtencion(self):
        if (self.proximoFinAtencion1 is not None and self.proximoFinAtencion2 is not None):
            if (self.proximoFinAtencion1 < self.proximoFinAtencion2):
                return self.proximoFinAtencion1
            return self.proximoFinAtencion2
        return None

    def finAtencion(self, proximoFinAtencion):
        if (proximoFinAtencion == self.proximoFinAtencion1):
            self.cliente1.finalizarAtencion(self.proximoFinAtencion1)
            self.cliente1.salir(self.proximoFinAtencion1)
            cliente = copy.deepcopy(self.cliente1)
            self.cliente1 = None
            self.proximoFinAtencion1 = None
        else:
            self.cliente2.finalizarAtencion(self.proximoFinAtencion2)
            self.cliente2.salir(self.proximoFinAtencion2)
            cliente = copy.deepcopy(self.cliente2)
            self.cliente2 = None
            self.proximoFinAtencion2 = None

        self.cantidadAtendidos += 1
        return cliente

    def getNumeroCliente(self, segundo):
        if (segundo):
            if self.cliente2 is not None:
                return self.cliente2.numero
        else:
            if self.cliente1 is not None:
                return self.cliente1.numero
        return "-"

    def getProximoFinAtencionString(self):
        proximoFinAtencion = self.getProximoFinAtencion()
        if proximoFinAtencion is not None:
            return proximoFinAtencion.time()
        return "-"

