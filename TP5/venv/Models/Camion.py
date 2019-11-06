import random

class Camion:
    # variables comunes a todos los objetos Camion
    cantidadTotal = 0

    def __init__(self, camionPropio, horaLlegada):
        self.nroCamion = Camion.cantidadTotal + 1
        Camion.cantidadTotal += 1
        self.propio = camionPropio
        self.horaLlegada = horaLlegada
        self.estado = "En cola recepcion"
        self.horaInicioEvento = 0
        self.horaFinEvento = 0
        self.litros = 0

    def getPropio(self):
        return self.propio

    def getHoraEntrada(self):
        return self.horaEntrada

    def getHoraLlegada(self):
        return self.horaLlegada

    def getHoraInicioEvento(self):
        return self.horaInicioEvento

    def getHoraFinEvento(self):
        return self.horaFinEvento

    def getEstado(self):
        return self.estado

    def getnroCamion(self):
        if self.nroCamion is not None:
            return self.nroCamion
        else:
            return ""

    def setHoraSalida(self, hora):
        self.horaSalida = hora

    def setHoraEntrada(self, hora):
        self.horaEntrada = hora

    def setEstado(self, estado):
        self.estado = estado

    def setHoraInicioEvento(self, horaInicioEvento):
        self.horaInicioEvento = horaInicioEvento

    def setHoraFinEvento(self, horaFinEvento):
        self.horaFinEvento = horaFinEvento

    def avanzarPosicion(self):
        self.posicion -= 1
        return True

    def setLitros(self, l):
        self.litros = l

    def getLitros(self):
        return self.litros
