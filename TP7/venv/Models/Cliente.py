from datetime import timedelta
from datetime import datetime

class Cliente():

    def __init__(self, numero):
        self.numero = numero
        self.estado = "Creado"
        self.tiempoAtencion = datetime(1, 1, 1, 0, 0, 0)
        self.horaLlegada = None
        self.horaInicioAtencion = None
        self.horaFinAtencion = None
        self.horaSalida = None
        self.tiempoEnSistema = None

    def llegar(self, horaLlegada):
        self.estado = "Llegando"
        self.horaLlegada = horaLlegada

    def comenzarAtencion(self, horaInicioAtencion, servidor):
        self.horaInicioAtencion = horaInicioAtencion
        self.estado = "En servidor " + servidor

    def finalizarAtencion(self, horaFinAtencion):
        self.horaFinAtencion = horaFinAtencion
        self.tiempoAtencion += self.horaFinAtencion - self.horaInicioAtencion

    def agregarACola(self, cola):
        self.estado = "En cola de " + cola

    def salir(self, horaSalida):
        self.horaSalida = horaSalida
        self.tiempoEnSistema = self.horaSalida - self.horaLlegada

    def tiempoDeEspera(self):
        return self.tiempoEnSistema - self.tiempoAtencion
