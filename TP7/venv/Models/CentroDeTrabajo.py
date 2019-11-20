from Models.Distribucion import IDistribucion
from datetime import datetime
from datetime import timedelta
from collections import deque
import copy

class CentroDeTrabajo():
    
    def __init__(self, distribucionAtencion, nombre, cola):
        self.distribucionAtencion = distribucionAtencion
        self.cola = cola
        self.cliente = None
        self.nombre = nombre
        self.estado = "Libre"
        self.cantidadAtendidos = 0
        self.cantidadAtendidosConEspera = 0
        self.proximoFinAtencion = datetime(100, 1, 1, 0, 0, 0)
        self.horaInicioBloqueo = None
        self.horaFinBloqueo = None
        self.tiempoEnEspera = 0
    
    def estaLibre(self):
        #return "Libre" in self.estado
        return self.estado == "Libre"

    def estaBloqueado(self):
        return self.estado.startswith("Bloqueado")
    
    def actualizarFinAtencion(self, hora):
        demora = round(self.distribucionAtencion.generar() * 60, 0)
        self.proximoFinAtencion = hora + timedelta(seconds=demora)

    def llegadaDeCliente(self, hora, cliente):
        if(self.estaLibre()):
            self.cliente = cliente
            self.estado = "Atendiendo a " + str(cliente.numero)
            cliente.comenzarAtencion(hora, self.nombre)
            self.actualizarFinAtencion(hora)
        else:
            if(self.estado == "Bloqueado - Libre"):
                self.cliente = cliente
                self.estado = "Bloqueado - Atendiendo a " + str(cliente.numero)
                cliente.comenzarAtencion(hora, self.nombre)
                self.actualizarFinAtencion(hora)
            self.cola.append(cliente)

    def tomarUnCliente(self):
        if (len(self.cola) == 0):
            self.estado = "Libre"
            self.cliente = None
            self.proximoFinAtencion = None
        else:
            self.cliente = self.cola.popleft()
            self.estado = "Atendiendo a " + str(self.cliente.numero)
            self.cliente.comenzarAtencion(self.proximoFinAtencion, self.nombre)
            self.actualizarFinAtencion(self.proximoFinAtencion)

    def finAtencion(self):
        cliente = copy.deepcopy(self.cliente)
        self.cliente.finalizarAtencion(self.proximoFinAtencion)
        self.cantidadAtendidos += 1

        if (self.horaFinBloqueo is not None):
            self.estado = "Bloqueado - En espera"
            self.cliente = None
            self.proximoFinAtencion = None
        else:
            self.tomarUnCliente()

        return cliente

    def bloquear(self, reloj, proxFinAtencionB):
        if (len(self.cola) == 0 and self.cliente is None):
            self.estado = "Bloqueado - Libre"
        else:
            self.estado = "Bloqueado - Atendiendo a " + str(self.cliente.numero)

        self.cantidadAtendidosConEspera += 1

        deltaEspera = (proxFinAtencionB - reloj).total_seconds()
        self.tiempoEnEspera = (self.tiempoEnEspera * (self.cantidadAtendidosConEspera - 1) + deltaEspera) / self.cantidadAtendidosConEspera

        self.horaInicioBloqueo = reloj
        self.horaFinBloqueo = proxFinAtencionB

    def actualizarFinBloqueo(self):
        cliente = copy.deepcopy(self.cliente)
        self.horaInicioBloqueo = None
        return cliente

    def finalizarBloqueo(self):
        horaFinBloqueo = copy.deepcopy(self.horaFinBloqueo)
        self.horaFinBloqueo = None

        if (self.estado.startswith("Bloqueado - At")):
            self.estado = "Atendiendo a " + str(self.cliente.numero)
        elif (self.estado.startswith("Bloqueado - Li") or self.estado.startswith("Bloqueado - En")):
            self.estado = "Libre"

        if (self.cliente is not None):
            cliente = copy.deepcopy(self.cliente)
            return cliente
        else:
            self.proximoFinAtencion = horaFinBloqueo
            self.tomarUnCliente()
            cliente = copy.deepcopy(self.cliente)
            return cliente

    def getNumeroCliente(self):
        if self.cliente is not None:
            return self.cliente.numero
        return "-"

    def getProximoFinAtencionString(self):
        if self.proximoFinAtencion is not None:
            return self.proximoFinAtencion.time()
        return "-"

    def getProximoFin(self):
        if (self.horaFinBloqueo is not None):
            return self.horaFinBloqueo
        if (self.proximoFinAtencion is not None):
            return self.proximoFinAtencion

