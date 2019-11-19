from Models.Distribucion import DistribucionExponencialNegativa
from Models.Distribucion import DistribucionNormal
from Models.Distribucion import DistribucionUniforme
from Models.CentroDeTrabajo import CentroDeTrabajo
from Models.MaestroSecador import MaestroSecador
from Models.Secador import Secador
from Models.Cliente import Cliente
from Models.Evento import Evento
from Models.Ingreso import Ingreso
import math
from datetime import datetime
from datetime import timedelta
import csv
import os

from collections import deque
_lambdaLlegadas = 12
_a = 1
_b = 10
_media = 8
_desvEstandar = 5
_varianza = math.pow(_desvEstandar, 2)

_distribucionIngreso = DistribucionExponencialNegativa(_lambdaLlegadas)
_distribucionCentroA = DistribucionUniforme(_a, _b)
_distribucionCentroB = DistribucionNormal(_media, _desvEstandar)
_distribucionSecado1 = DistribucionUniforme(120,121)
_distribucionSecado2 = DistribucionUniforme(130,131)

_colaIngreso = deque()
_colaCentroB = deque()

_ingreso = Ingreso(_distribucionIngreso)
_centroA = CentroDeTrabajo(_distribucionCentroA, "Centro de trabajo A", _colaIngreso)
_centroB = CentroDeTrabajo(_distribucionCentroB, "Centro de trabajo B", _colaCentroB)
_S1 = Secador(_distribucionSecado1, _distribucionSecado2, "Secador 1")
_S2 = Secador(_distribucionSecado1, _distribucionSecado2, "Secador 2")
_S3 = Secador(_distribucionSecado1, _distribucionSecado2, "Secador 3")
_S4 = Secador(_distribucionSecado1, _distribucionSecado2, "Secador 4")
_S5 = Secador(_distribucionSecado1, _distribucionSecado2, "Secador 5")
_maestroSecador = MaestroSecador(_S1, _S2,  _S3,  _S4,  _S5)

_listaCentros = [_centroA, _centroB]
_listaSecadores = [_S1, _S2,  _S3,  _S4,  _S5]

promedioPermanencia = 0.0
promedioAtencion = 0.0
tiempoEsperaA = 0.0
tiempoEsperaB = 0.0
numeroMaximoTrabajos = 0
resultado = []
atendidosCentroA = 0
permanenciaCentroA = 0.0
atendidosCentroB = 0
permanenciaCentroB = 0.0
atendidosSecado = 0
permanenciaSecado = 0

#hasta = int(input("Ingrese cuantos eventos desea procesar: "))

def simular(hasta):
    fila = 0
    reloj = datetime(1, 1, 1, hour=0, minute=0, second=0)
    trabajos = []
    numTrabajos = 0
    vectoresEstado = []

    while (hasta >= 0):
        hasta -= 1
        fila += 1

        # agregamos posibles eventos
        eventos = []
        eventos.append(Evento("Nuevo trabajo", _ingreso.proximaLlegada))
        eventos.extend(_maestroSecador.getEventos())
        eventos.append(Evento("Inicio de bloqueo B", _centroB.horaInicioBloqueo))
        eventos.append(Evento("Centro B desbloqueado", _centroB.horaFinBloqueo))
        eventos.append(Evento("Inicio de bloqueo A", _centroA.horaInicioBloqueo))
        eventos.append(Evento("Centro A desbloqueado", _centroA.horaFinBloqueo))
        eventos.append(Evento("Fin Centro B", _centroB.proximoFinAtencion))
        eventos.append(Evento("Fin Centro A", _centroA.proximoFinAtencion))

        # tomamos el primero
        eventoActual = eventos[0]

        # comparamos todos para tomar el minimo
        for evento in eventos:
            #print(evento.nombre + " - " + str(evento.hora.time()))
            if (evento.hora is not None):
                if (evento.hora < eventoActual.hora):
                    eventoActual = evento

        print(eventoActual.nombre + " - " + str(eventoActual.hora.time()))

        #actualizamos reloj
        reloj = eventoActual.hora

        if (eventoActual.nombre == "Nuevo trabajo"):
            numTrabajos += 1
            clienteLlegando = Cliente(numTrabajos)
            clienteLlegando.llegar(reloj)
            clienteEvento = clienteLlegando
            _centroA.llegadaDeCliente(reloj, clienteLlegando)
            _ingreso.actualizarIngreso()
            trabajos.append(clienteLlegando)

        elif (eventoActual.nombre == "Fin Centro B"):
            if (not _maestroSecador.hayLugar()):
                if (_centroB.horaFinBloqueo is not None):
                    clienteEvento = _centroB.finAtencion()
            if (_maestroSecador.hayLugar()):
                clienteEvento = _centroB.finAtencion()
                _maestroSecador.recibirCliente(reloj, clienteEvento)
                if (not _maestroSecador.hayLugar()):
                    if (_centroB.horaFinBloqueo is None):
                        _centroB.bloquear(reloj, _maestroSecador.getProximoFinAtencion())

        elif (eventoActual.nombre == "Fin Centro A"):
            if (len(_colaCentroB) == 3):
                if (_centroA.horaFinBloqueo is not None):
                    clienteEvento = _centroA.finAtencion()
            if (len(_colaCentroB) <= 2):
                clienteEvento = _centroA.finAtencion()
                _centroB.llegadaDeCliente(reloj, clienteEvento)
                if (len(_colaCentroB) == 3):
                    if (_centroA.horaFinBloqueo is None):
                        _centroA.bloquear(reloj, _centroB.proximoFinAtencion)

        elif (eventoActual.nombre == "Centro A desbloqueado"):
            clienteEvento = _centroA.finalizarBloqueo()

        elif (eventoActual.nombre == "Inicio de bloqueo A"):
            clienteEvento = _centroA.actualizarFinBloqueo()

        elif (eventoActual.nombre == "Centro B desbloqueado"):
            clienteEvento = _centroB.finalizarBloqueo()

        elif (eventoActual.nombre == "Inicio de bloqueo B"):
            clienteEvento = _centroB.actualizarFinBloqueo()

        elif (eventoActual.nombre == "Fin Secador 1"):
            clienteEvento = _maestroSecador.finAtencion(1, eventoActual.hora)

        elif (eventoActual.nombre == "Fin Secador 2"):
            clienteEvento = _maestroSecador.finAtencion(2, eventoActual.hora)

        elif (eventoActual.nombre == "Fin Secador 3"):
            clienteEvento = _maestroSecador.finAtencion(3, eventoActual.hora)

        elif (eventoActual.nombre == "Fin Secador 4"):
            clienteEvento = _maestroSecador.finAtencion(4, eventoActual.hora)

        elif (eventoActual.nombre == "Fin Secador 5"):
            clienteEvento = _maestroSecador.finAtencion(5, eventoActual.hora)

        vectorEstado = [fila,
                        reloj.time(),
                        eventoActual.nombre,
                        "-" if clienteEvento is None else clienteEvento.numero,
                        _ingreso.proximaLlegada.time(),
                        _listaCentros[0].estado,
                        _listaCentros[0].getNumeroCliente(),
                        _listaCentros[0].getProximoFinAtencionString(),
                        len(_listaCentros[0].cola),
                        _listaCentros[0].cantidadAtendidos,
                        _listaCentros[1].estado,
                        _listaCentros[1].getNumeroCliente(),
                        _listaCentros[1].getProximoFinAtencionString(),
                        len(_listaCentros[1].cola),
                        _listaCentros[1].cantidadAtendidos,
                        _maestroSecador.getLugares()]

        for trabajo in trabajos:
            vectorEstadoTrabajo = [trabajo.horaLlegada,
                                   trabajo.horaInicioAtencion,
                                   trabajo.horaFinAtencion,
                                   trabajo.horaSalida,
                                   trabajo.tiempoEnSistema]
            vectorEstado.extend(vectorEstadoTrabajo)

        vectoresEstado.append(vectorEstado)
    return vectoresEstado

vectoresEstado = simular(200)

result = open("Vectores estado.csv","w", newline="")
writer = csv.writer(result, delimiter=';')

for vector in vectoresEstado:
    writer.writerow(vector)
result.close()
