from Models.Camion import Camion
from Models.Servidor import Recepcion
from Models.Servidor import Balanza
from Models.Servidor import Darsena
from collections import deque
import math
import random
import time
import datetime
import csv
import os

print("Procesando estrategia 1...")

# creamos deques. Con append agregamos a la derecha, y con popleft sacamos desde la izquierda
colaRecepcion = deque()
colaBalanza = deque()
colaDarsena = deque()
colaTerminados = deque()

dia = 1
hora = 0
minutos = 0
segundos = 0
unoSobreLambda = 7.5 * 60 # 7,5 minutos
cantidadDuermenAfuera = deque([0]*30)
cantidadAtendidos = deque([0]*30)

tiempoTotalPermanencia=0
tiempoPromedioCamiones=0

#tiempolleg =0

servidorRecepcion = Recepcion()
servidorBalanza = Balanza()
servidorDarsena1 = Darsena()
servidorDarsena2 = Darsena()
atendidosrec=0
atendidosbal=0
atendidosdar1=0
atendidosdar2=0

agregadosColaRecepcion=0
agregadosColaBalanza=0
agregadosColaDar=0


# bandera que permite la llegada de camiones (entre las 12 hs y las 18)
flagLleganCamiones = False
flagRecibirCamiones = False

vectorEstados = deque()
vectorEstados.append(["", "", "", "", "", "Recepcion", "", "", "", "Balanza", "", "", "", "Darsena 1", "", "", "","Darsena 2"])
vectorEstados.append(["Evento", "Camion", "Dia", "Reloj", "Tiempo prox llegada", "Estado", "Camion", "Prox fin atencion", "Cola","Estado", "Camion", "Prox fin atencion", "Cola","Estado", "Camion", "Prox fin atencion","Estado", "Camion", "Prox fin atencion", "Cola"])

def convert_timedelta(seconds):
    duration = datetime.timedelta(seconds=int(seconds))
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds

def formatTime(time):
    return str(time[1]) + "hs " + str(time[2]) + "min " + str(time[3]) + "s"

def obtenerTiempoProxCamion():
    #formula gen var aleatoria exponencial
    t = (-unoSobreLambda) * math.log(1 - random.random(),math.e)
    t=round((t),0)
    return t

# tiempo en segundos hasta la llegada del proximo camion
proximoCamion = obtenerTiempoProxCamion()

while dia <= 3:
    proximoCamionS = 0
    finAtencionServRecS = None
    finAtencionServBalS = None
    finAtencionServDar1S = None
    finAtencionServDar2S = None

    # dia, hora, minuto y segundo actual
    d, h, m, s = convert_timedelta(segundos)

    # control del tiempo
    # avance de minutos
    if (segundos % 60 == 0):
        minutos += 1

    # prohibir llegada de camiones luego de las 18 clavados. Evita que lleguen durante las 18
    if (hora == 18 and minutos == 0 and segundos % 60 == 0):
        flagLleganCamiones = False

    # avance de horas
    if (segundos % 3600 == 0):
        minutos = 0
        # habilitar llegada de camiones. Se usan las 17 ya que la hora se actualiza al final
        if (hora >= 12 and hora <= 17):
            flagLleganCamiones = True
            # generacion vector de estados
            r = ["Apertura de puertas", "----", d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s", "----",
                 servidorRecepcion.getEstado(), "----", "----", str(len(colaRecepcion)),
                 servidorBalanza.getEstado(), "----", "----", str(len(colaBalanza)),
                 servidorDarsena1.getEstado(), "----", "----",
                 servidorDarsena2.getEstado(), "----", "----", str(len(colaDarsena))]
            vectorEstados.append(r)
            # fin generacion vector de estados
        else:
            flagLleganCamiones = False

        # almacenar la cantidad de camiones que duermen afuera
        if (hora >= 18):
           cantidadDuermenAfuera[dia-1]= len(colaRecepcion)

        # permitir recepcion de camiones
        if (hora >= 5 and hora <= 18 ):
            flagRecibirCamiones = True
            if (hora == 5):
                # generacion vector de estados
                r = ["Apertura de planta", "----", d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s", "----",
                     servidorRecepcion.getEstado(), "----", "----", str(len(colaRecepcion)),
                     servidorBalanza.getEstado(), "----", "----", str(len(colaBalanza)),
                     servidorDarsena1.getEstado(), "----", "----",
                     servidorDarsena2.getEstado(), "----", "----", str(len(colaDarsena))]
                vectorEstados.append(r)
                # fin generacion vector de estados
            if (hora == 18):
                # generacion vector de estados
                r = ["Cierre de planta", "----", d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s",  "----",
                     servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), formatTime(servidorRecepcion.gettiempoFinAtencion()), str(len(colaRecepcion)),
                     servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), formatTime(servidorBalanza.gettiempoFinAtencion()), str(len(colaBalanza)),
                     servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), formatTime(servidorDarsena1.gettiempoFinAtencion()),
                     servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), formatTime(servidorDarsena2.gettiempoFinAtencion())]
                vectorEstados.append(r)
                # fin generacion vector de estados
        else:
            flagRecibirCamiones = False

        # avanzar dias
        if (hora == 24):
            cantidadAtendidos[dia-1] = atendidosdar2 + atendidosdar1
            atendidosdar1 = 0
            atendidosdar2 = 0
            atendidosrec = 0
            atendidosbal = 0
            hora = 0
            dia += 1

        hora += 1

    #si esta entre las 12 y las 18, siguen llegando camiones
    if (flagLleganCamiones):
        if (proximoCamion > 0):
            proximoCamion -= 1
        else:
            camion = Camion(random.random() < 0.35)
            colaRecepcion.append(camion)
            agregadosColaRecepcion+=1
            # generacion vector de estados
            proximoCamion = obtenerTiempoProxCamion()
            proximoCamionS = proximoCamion
            d2, h2, m2, s2 = convert_timedelta(proximoCamionS)
            r = ["Llega camion", camion.getnroCamion(), d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s", str(h2) + "hs " + str(m2) + "min " + str(s2) + "s",
                 servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), formatTime(servidorRecepcion.gettiempoFinAtencion()), str(len(colaRecepcion)),
                 servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), formatTime(servidorBalanza.gettiempoFinAtencion()), str(len(colaBalanza)),
                 servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), formatTime(servidorDarsena1.gettiempoFinAtencion()),
                 servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), formatTime(servidorDarsena2.gettiempoFinAtencion()), str(len(colaDarsena))]
            vectorEstados.append(r)
            # fin generacion vector de estados
    else:
        proximoCamion = obtenerTiempoProxCamion()

    # si recepcion esta atendiendo a alguien lo sigue atendiendo, pero no recibe camiones pasadas las 18hs
    if (flagRecibirCamiones):
        c = servidorRecepcion.obtenerEvento()
        if (c is not None):
            finAtencionServRecS = None
            if (c.getPropio()):
                colaDarsena.append(c)
                agregadosColaDar+=1
            else:
                colaBalanza.append(c)
                agregadosColaBalanza+=1
            if(len(colaRecepcion) > 0):
                if (flagRecibirCamiones):
                    cam=colaRecepcion.popleft()
                    cam.setHoraEntrada(segundos)
                    servidorRecepcion.recibirCamion(cam)
                    finAtencionServRecS = servidorRecepcion.gettiempoFinAtencion()
                    atendidosrec += 1
            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if ( finAtencionServRecS is not None):
                d2, h2, m2, s2 = finAtencionServRecS
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            r = ["Fin atencion Recepcion", c.getnroCamion(), d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s",
                 str(h3) + "hs " + str(m3) + "min " + str(s3) + "s",
                 servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", str(len(colaRecepcion)),
                 servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), formatTime(servidorBalanza.gettiempoFinAtencion()), str(len(colaBalanza)),
                 servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), formatTime(servidorDarsena1.gettiempoFinAtencion()),
                 servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), formatTime(servidorDarsena2.gettiempoFinAtencion()), str(len(colaDarsena))]
            vectorEstados.append(r)
            # fin generacion vector de estados

        if (not servidorRecepcion.getOcupado()):
            if (len(colaRecepcion) > 0):
                cam=colaRecepcion.popleft()
                cam.setHoraEntrada(segundos)
                servidorRecepcion.recibirCamion(cam)
                atendidosrec += 1

    #La atencion de camiones se hace durante todo el dia
    #servidor balanza
    cBalanza = servidorBalanza.obtenerEvento()
    if (cBalanza is not None):
        finAtencionServBalS = None
        colaDarsena.append(cBalanza)
        if(len(colaBalanza) > 0):
            servidorBalanza.recibirCamion(colaBalanza.popleft())
            atendidosbal += 1

        # generacion vector de estados
        d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
        if (finAtencionServBalS is not None):
            d2, h2, m2, s2 = convert_timedelta(finAtencionServBalS)
        else:
            h2 = ".."
            m2 = ".."
            s2 = ".."
        r = ["Fin atencion Balanza", cBalanza.getnroCamion(), d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s",
             str(h3) + "hs " + str(m3) + "min " + str(s3) + "s",
             servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), formatTime(servidorRecepcion.gettiempoFinAtencion()), str(len(colaRecepcion)),
             servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", str(len(colaBalanza)),
             servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), formatTime(servidorDarsena1.gettiempoFinAtencion()),
             servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), formatTime(servidorDarsena2.gettiempoFinAtencion()), str(len(colaDarsena))]
        vectorEstados.append(r)
        # fin generacion vector de estados


    if (not servidorBalanza.getOcupado()):
        if (len(colaBalanza) > 0):
            servidorBalanza.recibirCamion(colaBalanza.popleft())
            atendidosbal += 1

    #servidores darsena
    cDarsena1 = servidorDarsena1.obtenerEvento()
    cDarsena2 = servidorDarsena2.obtenerEvento()
    #ver a que darsena le tengo q pasar un camion
    if (len(colaDarsena) >= 1):
        if (isinstance(cDarsena1, Camion)):
            finAtencionServDar1S = None
            cDarsena1.setHoraSalida(segundos)
            colaTerminados.append(cDarsena1)
            servidorDarsena1.recibirCamion(colaDarsena.popleft())
            finAtencionServDar1S = servidorDarsena1.gettiempoFinAtencion()
            atendidosdar1 += 1

            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if (finAtencionServDar1S is not None):
                d2, h2, m2, s2 = finAtencionServDar1S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            r = ["Fin atencion Darsena 1", cDarsena1.getnroCamion(), d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s",
                 str(h3) + "hs " + str(m3) + "min " + str(s3) + "s",
                 servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), formatTime(servidorRecepcion.gettiempoFinAtencion()), str(len(colaRecepcion)),
                 servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), formatTime(servidorBalanza.gettiempoFinAtencion()), str(len(colaBalanza)),
                 servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), str(h2) + "hs " + str(m2) + "min " + str(s2) + "s",
                 servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), formatTime(servidorDarsena2.gettiempoFinAtencion()), str(len(colaDarsena))]
            vectorEstados.append(r)
            # fin generacion vector de estados

        if (isinstance(cDarsena2, Camion)):
            finAtencionServDar2S = None
            cDarsena2.setHoraSalida(segundos)
            colaTerminados.append(cDarsena2)
            servidorDarsena2.recibirCamion(colaDarsena.popleft())
            finAtencionServDar2S = servidorDarsena1.gettiempoFinAtencion()
            atendidosdar2 += 1

            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if (finAtencionServDar2S is not None):
                d2, h2, m2, s2 = finAtencionServDar2S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            r = ["Fin atencion Darsena 2", cDarsena2.getnroCamion(), d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s",
                 str(h3) + "hs " + str(m3) + "min " + str(s3) + "s",
                 servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), formatTime(servidorRecepcion.gettiempoFinAtencion()), str(len(colaRecepcion)),
                 servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), formatTime(servidorBalanza.gettiempoFinAtencion()), str(len(colaBalanza)),
                 servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), formatTime(servidorDarsena1.gettiempoFinAtencion()),
                 servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", str(len(colaDarsena))]
            vectorEstados.append(r)
            # fin generacion vector de estados
    else:
        if (isinstance(cDarsena1, Camion)):
            finAtencionServDar1S = None
            cDarsena1.setHoraSalida(segundos)
            colaTerminados.append(cDarsena1)
            atendidosdar1 += 1

            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if (finAtencionServDar1S is not None):
                d2, h2, m2, s2 = convert_timedelta(finAtencionServDar1S)
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            r = ["Fin atencion Darsena 1", cDarsena1.getnroCamion(), d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s",
                 str(h3) + "hs " + str(m3) + "min " + str(s3) + "s",
                 servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), formatTime(servidorRecepcion.gettiempoFinAtencion()), str(len(colaRecepcion)),
                 servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), formatTime(servidorBalanza.gettiempoFinAtencion()), str(len(colaBalanza)),
                 servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), str(h2) + "hs " + str(m2) + "min " + str(s2) + "s",
                 servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), formatTime(servidorDarsena2.gettiempoFinAtencion()), str(len(colaDarsena))]
            vectorEstados.append(r)
            # fin generacion vector de estados

        if (isinstance(cDarsena2, Camion)):
            finAtencionServDar2S = None
            colaTerminados.append(cDarsena2)
            cDarsena2.setHoraSalida(segundos)
            atendidosdar2 += 1

            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if (finAtencionServDar2S is not None):
                d2, h2, m2, s2 = convert_timedelta(finAtencionServDar2S)
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            r = ["Fin atencion Darsena 2", cDarsena2.getnroCamion(), d + 1, str(h) + "hs " + str(m) + "min " + str(s) + "s",
                 str(h3) + "hs " + str(m3) + "min " + str(s3) + "s",
                 servidorRecepcion.getEstado(), servidorRecepcion.getNroCliente(), formatTime(servidorRecepcion.gettiempoFinAtencion()), str(len(colaRecepcion)),
                 servidorBalanza.getEstado(), servidorBalanza.getNroCliente(), formatTime(servidorBalanza.gettiempoFinAtencion()), str(len(colaBalanza)),
                 servidorDarsena1.getEstado(), servidorDarsena1.getNroCliente(), formatTime(servidorDarsena1.gettiempoFinAtencion()),
                 servidorDarsena2.getEstado(), servidorDarsena2.getNroCliente(), str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", str(len(colaDarsena))]
            vectorEstados.append(r)
            # fin generacion vector de estados


    if (not servidorDarsena1.getOcupado()):
        if (len(colaDarsena) > 0):
            servidorDarsena1.recibirCamion(colaDarsena.popleft())
            atendidosdar1 += 1

    if (not servidorDarsena2.getOcupado()):
        if (len(colaDarsena) > 0):
            servidorDarsena2.recibirCamion(colaDarsena.popleft())
            atendidosdar2 += 1

    segundos += 1

#calculamos promedio de tiempo permanencia camiones
for i in colaTerminados:
    tiempoTotalPermanencia += (i.horaSalida-i.horaEntrada)

tiempoPromedioCamiones = round(tiempoTotalPermanencia/len(colaTerminados),0)

# lo pasamos a una cadena más entendible
days, hours, minutes, seconds = convert_timedelta(tiempoPromedioCamiones)
strTiempoPromedioCamiones = str(hours) + "hs " + str(minutes) + "min " + str(seconds) + "s"

#creamos un array de dias
i = 2
dias = []
dias.append("Días")
while i < 32:
    dias.append("Día " + str(i-1))
    i += 1

cantidadAtendidos.appendleft("Cant. atendidos p/día")
cantidadDuermenAfuera.appendleft("Cant. duermen afuera p/día")

#exportacion csv
result = open("Resultados.csv","w", newline="")
writer = csv.writer(result, delimiter=';')

writer.writerow(["1er estrategia"])
writer.writerow([""])
writer.writerow(dias)
writer.writerow(cantidadAtendidos)
writer.writerow(cantidadDuermenAfuera)
writer.writerow([""])
writer.writerow(["Tiempo de permanencia promedio",strTiempoPromedioCamiones])
result.close()

#exportacion csv
result = open("Vector estados 1er estrategia.csv","w", newline="")
writer = csv.writer(result, delimiter=';')

for evento in vectorEstados:
    writer.writerow(evento)
result.close()

print("Listo")

os.system('python Orquestador2daEstrategia.py')
