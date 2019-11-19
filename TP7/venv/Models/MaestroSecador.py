from Models.Distribucion import IDistribucion
from Models.Evento import Evento
from datetime import datetime
from datetime import timedelta
from collections import deque
import copy

class MaestroSecador():

    def __init__(self, s1, s2, s3, s4, s5):
        self.secadores = [s1, s2, s3, s4, s5]
        self.colas = [deque(), deque(), deque(), deque(), deque()]

    def getEventos(self):
        eventos = []
        for secador in self.secadores:
            if (secador.getProximoFinAtencion() is not None):
                eventos.append(Evento("Fin " + secador.nombre, secador.getProximoFinAtencion()))
        return eventos

    def hayLugar(self):
        if (len(self.colas[0]) + len(self.colas[1]) + len(self.colas[2]) + len(self.colas[3]) + len(self.colas[4]) < 10):
            print(len(self.colas[0]) + len(self.colas[1]) + len(self.colas[2]) + len(self.colas[3]) + len(self.colas[4]))
            return True
        return False

    def recibirCliente(self, reloj, cliente):
        for i in range(0, 5):
            if(len(self.colas[i]) == 0):
                self.colas[i].append(cliente)
                self.secadores[i].llegadaDeCliente(reloj, self.colas[i][0])
                return

        for x in range(0, 5):
            if(len(self.colas[x]) == 1):
                self.colas[x].append(cliente)
                self.secadores[x].llegadaDeCliente(reloj, self.colas[x][1])
                return
            
        raise IndexError

    def getProximoFinAtencion(self):
        proximoFinAtencion = datetime(100, 1, 1, 0, 0, 0)
        for secador in self.secadores:
            if secador.getProximoFinAtencion() < proximoFinAtencion:
                proximoFinAtencion = secador.getProximoFinAtencion()

        return proximoFinAtencion

    def finAtencion(self, nroSecador, proximoFinAtencion):
        secador = self.secadores[nroSecador - 1]
        cliente = secador.finAtencion(proximoFinAtencion)

        if (self.colas[nroSecador - 1][0] == cliente.numero):
            self.colas[nroSecador - 1].popleft()
        else:
            self.colas[nroSecador - 1].pop()

        return cliente

    def getLugares(self):
        lugares = 0
        for cola in self.colas:
            lugares += len(cola)
        return "Quedan " + str(lugares)
