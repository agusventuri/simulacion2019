from Models.Distribucion import DistribucionExponencialNegativa
from Models.Distribucion import DistribucionNormal
from Models.Distribucion import DistribucionUniforme
from Models.Distribucion import DiffUnTrabajo
from Models.Distribucion import DiffDosTrabajo
from Models.CentroDeTrabajo import CentroDeTrabajo
from Models.MaestroSecador import MaestroSecador
from Models.Secador import Secador
from Models.Cliente import Cliente
from Models.Evento import Evento
from Models.Ingreso import Ingreso
import math
import openpyxl
from openpyxl.styles.borders import Border, Side
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
#_distribucionSecado1 = DistribucionUniforme(100,105)
#_distribucionSecado2 = DistribucionUniforme(120,125)
_distribucionSecado1 = DiffUnTrabajo()
_distribucionSecado2 = DiffDosTrabajo()

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

#hasta = int(input("Ingrese cuantos eventos desea procesar: "))

def simular(opcion, cantidad):
    if (opcion == 1):
        hasta = cantidad
    elif (opcion == 2):
        hasta = 1
        horaLimite = datetime(1, 1, 1, hour = cantidad, minute = 0, second = 0)
    else:
        hasta = 1
    fila = -1
    reloj = datetime(1, 1, 1, hour=0, minute=0, second=0)
    trabajos = []
    numTrabajos = 0
    numTrabajosTerminados = 0
    maxHastaAhora = 0
    promedioAtencion = 0
    cantidadEnTaller = 0
    vectoresEstado = []
    vectoresEstado.append(["", "", "", "", "", "", "",
                           "Centro de atencion A", "", "", "", "", "",
                           "Centro de atencion B", "", "", "", "", "",
                           "",
                           "Secador nro 1", "", "", "1",
                           "Secador nro 2", "", "", "",
                           "Secador nro 3", "", "", "",
                           "Secador nro 4", "", "", "",
                           "Secador nro 5", "", "", "",
                           ""])
    vectoresEstado.append(["#", "Reloj", "Evento", "Cliente", "Próxima llegada", "Cant actual", "Max",
                           "Estado", "Cliente", "Prox fin", "Cant cola", "Cant atendidos", "Espera promedio",
                           "Estado", "Cliente", "Prox fin", "Cant cola", "Cant atendidos", "Espera promedio",
                           "Lugares en secadores",
                           "Estado", "Cliente 1", "Cliente 2", "Prox fin",
                           "Estado", "Cliente 1", "Cliente 2", "Prox fin",
                           "Estado", "Cliente 1", "Cliente 2", "Prox fin",
                           "Estado", "Cliente 1", "Cliente 2", "Prox fin",
                           "Estado", "Cliente 1", "Cliente 2", "Prox fin",
                           "Promedio t atencion"])

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
        eventos.append(Evento("Fin Centro B", _centroB.proximoFinAtencion))
        eventos.append(Evento("Centro A desbloqueado", _centroA.horaFinBloqueo))
        eventos.append(Evento("Fin Centro A", _centroA.proximoFinAtencion))

        # tomamos el primero
        eventoActual = eventos[0]

        # comparamos todos para tomar el minimo
        for evento in eventos:
            if (evento.hora is not None):
                if (evento.hora < eventoActual.hora):
                    eventoActual = evento

        #actualizamos reloj
        reloj = eventoActual.hora

        if (opcion == 2 and reloj > horaLimite):
            break
        else:
            if(opcion == 2 and reloj < horaLimite):
                hasta = 1

        if (opcion == 3):
            hasta = 1

        if (eventoActual.nombre == "Nuevo trabajo"):
            cantidadEnTaller += 1
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
                else:
                    _centroA.bloquear(reloj, _centroB.getProximoFin())
            if (len(_colaCentroB) <= 2):
                clienteEvento = _centroA.finAtencion()
                _centroB.llegadaDeCliente(reloj, clienteEvento)
                if (len(_colaCentroB) == 3):
                    if (_centroA.horaFinBloqueo is None):
                        _centroA.bloquear(reloj, _centroB.getProximoFin())

        elif (eventoActual.nombre == "Centro A desbloqueado"):
            clienteEvento = _centroA.finalizarBloqueo()

        elif (eventoActual.nombre == "Inicio de bloqueo A"):
            clienteEvento = _centroA.actualizarFinBloqueo()

        elif (eventoActual.nombre == "Centro B desbloqueado"):
            clienteEvento = _centroB.finalizarBloqueo()

        elif (eventoActual.nombre == "Inicio de bloqueo B"):
            clienteEvento = _centroB.actualizarFinBloqueo()

        elif(eventoActual.nombre.startswith("Fin Secador")):
            cantidadEnTaller -= 1
            numTrabajosTerminados += 1
            nroSecador = int(eventoActual.nombre[-1:])
            clienteEvento = _maestroSecador.finAtencion(nroSecador, eventoActual.hora)
            tEnSistema = clienteEvento.tiempoEnSistema.total_seconds()
            promedioAtencion = (promedioAtencion * (numTrabajosTerminados - 1) + tEnSistema) / numTrabajosTerminados
            if (opcion == 3 and numTrabajosTerminados == cantidad):
                hasta = -1

        if (cantidadEnTaller > maxHastaAhora):
            maxHastaAhora = cantidadEnTaller

        for index, trabajoViejo in enumerate(trabajos):
            if (clienteEvento is not None and trabajoViejo.numero == clienteEvento.numero):
                trabajos[index] = clienteEvento

        vectorEstado = [fila,
                        reloj.time(),
                        eventoActual.nombre,
                        "-" if clienteEvento is None else clienteEvento.numero,
                        _ingreso.proximaLlegada.time(),
                        cantidadEnTaller,
                        maxHastaAhora]

        for centro in _listaCentros:
            vectorEstado.extend([centro.estado,
                                 centro.getNumeroCliente(),
                                 centro.getProximoFinAtencionString(),
                                 len(centro.cola),
                                 centro.cantidadAtendidos,
                                 timedelta(seconds=round(centro.tiempoEnEspera, 0))])

        vectorEstado.append(_maestroSecador.getLugares())

        for secador in _listaSecadores:
            vectorEstado.extend([secador.estado,
                                   secador.getNumeroCliente(False),
                                   secador.getNumeroCliente(True),
                                   secador.getProximoFinAtencionString()])

        vectorEstado.append(timedelta(seconds=round(promedioAtencion, 0)))

        for trabajo in trabajos:
            vectorEstado.extend([trabajo.estado,
                                   "-" if trabajo.horaLlegada is None else trabajo.horaLlegada.time(),
                                   "-" if trabajo.horaInicioAtencion is None else trabajo.horaInicioAtencion.time(),
                                   "-" if trabajo.horaFinAtencion is None else trabajo.horaFinAtencion.time(),
                                   "-" if trabajo.horaSalida is None else trabajo.horaSalida.time(),
                                   "-" if trabajo.tiempoEnSistema is None else trabajo.tiempoEnSistema])

        vectoresEstado.append(vectorEstado)
    return vectoresEstado, trabajos

print("Ingresa una opción para establecer el final de la simulacion: ")
print("\t1 - Eventos")
print("\t2 - Horas")
print("\t3 - Trabajos")
opcion = int(input("-> "))
opcionStr = "eventos" if opcion == 1 else "horas" if opcion == 2 else "trabajos"
cantidad = int(input("Ahora ingrese la cantidad de " + opcionStr + " a procesar: "))
print("\nProcesando....\n")

vectoresEstado, trabajos = simular(opcion, cantidad)

print("Listo :)\n")
print("Ingresa una opción a imprimir: ")
print("\t1 - CSV")
print("\t2 - Excel")
print("\t3 - Ambos")

opcion = int(input("-> "))

for trabajo in trabajos:
    vectoresEstado[0].extend(["Trabajo", "Nro", "", "", "", trabajo.numero])
    vectoresEstado[1].extend(["Estado", "Llegada", "Inicio atención", "Fin atención", "Salida", "Tiempo en sistema"])

largoTotal = len(vectoresEstado[0])

for vector in vectoresEstado:
    vector.extend((largoTotal-len(vector)) * [""])

if (opcion == 1 or opcion == 3):
    result = open("Vectores estado.csv","w", newline="")
    writer = csv.writer(result, delimiter=';')

    for vector in vectoresEstado:
        writer.writerow(vector)
    result.close()

if (opcion == 2 or opcion == 3):
    # creamos el archivo en excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Vector estados"

    borderLeft = Border(left=Side(border_style="thin"),
                        right=Side(border_style=None),
                        top=Side(border_style=None),
                        bottom=Side(border_style=None))
    borderBottom = Border(left=Side(border_style=None),
                        right=Side(border_style=None),
                        top=Side(border_style=None),
                        bottom=Side(border_style="thin"))
    borderBottomLeft = Border(left=Side(border_style="thin"),
                        right=Side(border_style=None),
                        top=Side(border_style=None),
                        bottom=Side(border_style="thin"))

    for fila, vector in enumerate(vectoresEstado):
        for columna, item in enumerate(vector):
            sheet.cell(row=fila + 1, column=columna + 1).value = str(item)
            c = columna + 1
            f = fila + 1
            if (c == 8 or c == 14 or c == 20 or c == 21 or c == 25 or c == 29 or c == 33 or c == 37 or c == 41 or
                    (c >= 42 and c%6 == 0)):
                sheet.cell(row=f, column=c).border = borderLeft
            if (f == 1 or f == 2):
                if (sheet.cell(row=f, column=c).border.left.border_style == "thin"):
                    sheet.cell(row=f, column=c).border = borderBottomLeft
                else:
                    sheet.cell(row=f, column=c).border = borderBottom

    sheet.merge_cells(start_row=1, start_column=8, end_row=1, end_column=13)
    sheet.merge_cells(start_row=1, start_column=14, end_row=1, end_column=19)
    sheet.merge_cells(start_row=1, start_column=21, end_row=1, end_column=24)
    sheet.merge_cells(start_row=1, start_column=25, end_row=1, end_column=28)
    sheet.merge_cells(start_row=1, start_column=29, end_row=1, end_column=32)
    sheet.merge_cells(start_row=1, start_column=33, end_row=1, end_column=36)
    sheet.merge_cells(start_row=1, start_column=37, end_row=1, end_column=40)1

    wb.save("Vector estados excel.xlsx")
