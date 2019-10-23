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
minutos = -1
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
flagUltimoCamion = False

vectorEstados = deque()
vectorEstados.append(["", "", "", "", "", "Recepcion", "", "", "", "Balanza", "", "", "", "Darsena 1", "", "", "", "","Darsena 2", "", "", "", "Camion 1", "", "", "", "Camion 2", "", "", "", "Camion 3", "", "", "", "Camion 4", "", "", "", "Camion 5", "", "", "", "Camion 6", "", "", "", "Camion 7", "", "", "", "Camion 8", "", "", "", "Camion 9", "", "", "", "Camion 10", "", "", ""])
vectorEstados.append(["Evento", "Camion", "Dia", "Reloj", "Tiempo prox llegada", "Estado", "Camion", "Prox fin atencion", "Cola","Estado", "Camion", "Prox fin atencion", "Cola","Estado", "Camion", "Prox fin atencion", "Atendidos","Estado", "Camion", "Prox fin atencion", "Atendidos", "Cola", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion", "Estado", "Llegada", "Inicio atencion", "Fin atencion"])
camiones = []

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

def procesarCamiones(r):
    if len(camiones)>0:
        for c in camiones:
            dCamion1, hCamion1, mCamion1, sCamion1 = convert_timedelta(c.getHoraLlegada())
            dCamion2, hCamion2, mCamion2, sCamion2 = convert_timedelta(c.getHoraInicioEvento())
            dCamion3, hCamion3, mCamion3, sCamion3 = convert_timedelta(c.getHoraInicioEvento() + c.getHoraFinEvento())
            estado = c.getEstado()
            r.append(estado)
            if estado == "Terminado":
                r.extend(["--:--:--", "--:--:--", "--:--:--"])
            else:
                r.append(str(dCamion1) + "dias" + str(hCamion1) + "hs " + str(mCamion1) + "min " + str(sCamion1) + "s")
                r.append(str(dCamion2) + "dias" + str(hCamion2) + "hs " + str(mCamion2) + "min " + str(sCamion2) + "s")
                r.append(str(dCamion3) + "dias" + str(hCamion3) + "hs " + str(mCamion3) + "min " + str(sCamion3) + "s")

    for i in range(10 - len(camiones)):
        r.extend(["----", "----", "----", "----"])

    return r

def generarVectorDeEstados(evento, nroCamion, d, h, minutos, s, stringTiempoProxCamion,
                           boolNroCliente, boolTiempoFinAt, boolCantAtendidos,
                           finAtRecepcion, finAtBalanza, finAtDarsena1, finAtDarsena2):
    if boolNroCliente:
        nroCliente1 = servidorRecepcion.getNroCliente()
        nroCliente2 = servidorBalanza.getNroCliente()
        if evento == "Fin calibracion Darsena 1":
            nroCliente3 = "----"
        else:
            nroCliente3 = servidorDarsena1.getNroCliente()
        if evento == "Fin calibracion Darsena 2":
            nroCliente4 = "----"
        else:
            nroCliente4 = servidorDarsena2.getNroCliente()
    else:
        nroCliente1, nroCliente2, nroCliente3, nroCliente4 = "----", "----", "----", "----"

    if boolTiempoFinAt:
        if finAtRecepcion is not False:
            tiempoFinAt1 = finAtRecepcion
        else:
            tiempoFinAt1 = formatTime(servidorRecepcion.gettiempoFinAtencion())

        if finAtBalanza is not False:
            tiempoFinAt2 = finAtBalanza
        else:
            tiempoFinAt2 = formatTime(servidorBalanza.gettiempoFinAtencion())

        if finAtDarsena1 is not False:
            tiempoFinAt3 = finAtDarsena1
        else:
            tiempoFinAt3 = formatTime(servidorDarsena1.gettiempoFinAtencion())

        if finAtDarsena2 is not False:
            tiempoFinAt4 = finAtDarsena2
        else:
            tiempoFinAt4 = formatTime(servidorDarsena2.gettiempoFinAtencion())
    else:
        tiempoFinAt1, tiempoFinAt2, tiempoFinAt3, tiempoFinAt4 = "----", "----", "----", "----"

    if boolCantAtendidos:
        cantAtendidos1 = servidorDarsena1.getCamionesAtendidos()
        cantAtendidos2 = servidorDarsena2.getCamionesAtendidos()
    else:
        cantAtendidos1, cantAtendidos2 = "----", "----"

    r = [evento, nroCamion, d + 1, str(h) + "hs " + str(minutos) + "min " + str(s) + "s", stringTiempoProxCamion,
         servidorRecepcion.getEstado(), nroCliente1, tiempoFinAt1, str(len(colaRecepcion)),
         servidorBalanza.getEstado(), nroCliente2, tiempoFinAt2, str(len(colaBalanza)),
         servidorDarsena1.getEstado(), nroCliente3, tiempoFinAt3, cantAtendidos1,
         servidorDarsena2.getEstado(), nroCliente4, tiempoFinAt4, cantAtendidos2, str(len(colaDarsena))]
    return r

# tiempo en segundos hasta la llegada del proximo camion
proximoCamion = obtenerTiempoProxCamion()

while dia <= 30:
    proximoCamionS = 0
    finAtencionServRecS = None
    finAtencionServBalS = None
    finAtencionServDar1S = None
    finAtencionServDar2S = None

    # dia, hora, minuto y segundo actual
    d, h, m, s = convert_timedelta(segundos)

    # control del tiempo
    # prohibir llegada de camiones luego de las 18 clavados. Evita que lleguen durante las 18
    if (hora == 19 and minutos == 0 and segundos % 60 == 1):
        flagLleganCamiones = False

    # prohibir recepcion de camiones luego de las 18 clavados. Evita atenderlos durante las 18
    if (hora == 19 and minutos == 0 and segundos % 60 == 0):
        flagRecibirCamiones = False
        if (servidorRecepcion.getOcupado()):
            flagUltimoCamion = True

    # marcar la apertura de puertas
    if (hora == 13 and minutos == 0 and segundos % 60 == 0):
        proximoCamion = obtenerTiempoProxCamion()
        # generacion vector de estados
        r = generarVectorDeEstados("Apertura de puertas", "----", d, h, minutos, s, "----",
                                   False, False, False,
                                   False, False, False, False)
        r = procesarCamiones(r)
        vectorEstados.append(r)
        # fin generacion vector de estados

    # avance de horas
    if (segundos % 3600 == 0 and segundos % 60 == 0):
        minutos = -1
        # habilitar llegada de camiones.
        if (hora >= 12 and hora < 18):
            flagLleganCamiones = True
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
                r = generarVectorDeEstados("Apertura de planta", "----", d, h, minutos, s, "----",
                                   False, False, False,
                                   False, False, False, False)
                r = procesarCamiones(r)
                vectorEstados.append(r)
                # fin generacion vector de estados
            if (hora == 18):
                # generacion vector de estados
                r = generarVectorDeEstados("Cierre de planta", "----", d, h, m, s, "----",
                                           True, True, True,
                                           False, False, False, False)
                r = procesarCamiones(r)
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

    # avance de minutos
    if (segundos % 60 == 0):
        minutos += 1

    #si esta entre las 12 y las 18, siguen llegando camiones
    if (flagLleganCamiones):
        if (proximoCamion > 0):
            proximoCamion -= 1
        else:
            camion = Camion(random.random() < 0.35, segundos)
            camion.setEstado("En cola")
            if (len(camiones) < 10):
                camiones.append(camion)
            colaRecepcion.append(camion)
            camion.setHoraInicioEvento(segundos)
            agregadosColaRecepcion+=1
            # generacion vector de estados
            proximoCamion = obtenerTiempoProxCamion()
            proximoCamionS = proximoCamion
            d2, h2, m2, s2 = convert_timedelta(proximoCamionS)
            stringProxCamion = str(h2) + "hs " + str(m2) + "min " + str(s2) + "s"
            r = generarVectorDeEstados("Llega camion", str(camion.getnroCamion()), d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, False, False)
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados
    else:
        proximoCamion = obtenerTiempoProxCamion()

    # si recepcion esta atendiendo a alguien lo sigue atendiendo, pero no recibe camiones pasadas las 18hs
    if (flagRecibirCamiones or (flagUltimoCamion and servidorRecepcion.getOcupado())):
        c = servidorRecepcion.obtenerEvento()
        if (c is not None):
            c.setEstado("En cola")
            c.setHoraInicioEvento(segundos)
            finAtencionServRecS = None
            if (c.getPropio()):
                colaDarsena.append(c)
                agregadosColaDar+=1
            else:
                colaBalanza.append(c)
                agregadosColaBalanza+=1
            if(len(colaRecepcion) > 0 and not flagUltimoCamion):
                if (flagRecibirCamiones):
                    cam = colaRecepcion.popleft()
                    cam.setEstado("En servidor")
                    cam.setHoraEntrada(segundos)
                    servidorRecepcion.recibirCamion(cam)
                    finAtencionServRecS = servidorRecepcion.gettiempoFinAtencion()
                    cam.setHoraInicioEvento(segundos)
                    cam.setHoraFinEvento(servidorRecepcion.gettiempoFinAtencionSegundos())
                    atendidosrec += 1
            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if ( finAtencionServRecS is not None):
                d2, h2, m2, s2 = finAtencionServRecS
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            stringProxCamion = str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Fin atencion Recepcion", c.getnroCamion(), d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       str(h2) + "hs " + str(m2) + "min " + str(s2), False, False, False)
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados

        if (not servidorRecepcion.getOcupado() and not flagUltimoCamion):
            if (len(colaRecepcion) > 0):
                cam=colaRecepcion.popleft()
                cam.setHoraEntrada(segundos)
                cam.setEstado("En servidor")
                servidorRecepcion.recibirCamion(cam)
                cam.setHoraInicioEvento(segundos)
                cam.setHoraFinEvento(servidorRecepcion.gettiempoFinAtencionSegundos())
                atendidosrec += 1

        if (c is not None and flagUltimoCamion):
            flagUltimoCamion = False

    #La atencion de camiones se hace durante todo el dia
    #servidor balanza
    cBalanza = servidorBalanza.obtenerEvento()
    if (cBalanza is not None):
        cBalanza.setEstado("En cola")
        finAtencionServBalS = None
        colaDarsena.append(cBalanza)
        if(len(colaBalanza) > 0):
            cam = colaBalanza.popleft()
            cam.setEstado("En servidor")
            servidorBalanza.recibirCamion(cam)
            cam.setHoraInicioEvento(segundos)
            cam.setHoraFinEvento(servidorBalanza.gettiempoFinAtencionSegundos())
            atendidosbal += 1

        # generacion vector de estados
        d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
        if (finAtencionServBalS is not None):
            d2, h2, m2, s2 = convert_timedelta(finAtencionServBalS)
        else:
            h2 = ".."
            m2 = ".."
            s2 = ".."
        stringProxCamion = str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
        r = generarVectorDeEstados("Fin atencion Balanza", cBalanza.getnroCamion(), d, h, m, s, stringProxCamion,
                                   True, True, True,
                                   False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", False, False)
        r = procesarCamiones(r)
        vectorEstados.append(r)
        # fin generacion vector de estados


    if (not servidorBalanza.getOcupado()):
        if (len(colaBalanza) > 0):
            cam = colaBalanza.popleft()
            cam.setEstado("En servidor")
            servidorBalanza.recibirCamion(cam)
            cam.setHoraInicioEvento(segundos)
            cam.setHoraFinEvento(servidorBalanza.gettiempoFinAtencionSegundos())
            atendidosbal += 1

    #servidores darsena
    cDarsena1 = servidorDarsena1.obtenerEvento()
    cDarsena2 = servidorDarsena2.obtenerEvento()

    #ver a que darsena le tengo q pasar un camion
    if (len(colaDarsena) >= 1):
        if (isinstance(cDarsena1, Camion) and not servidorDarsena1.getCalibrando()):
            cDarsena1.setEstado("En cola")
            finAtencionServDar1S = None
            cDarsena1.setHoraSalida(segundos)
            cDarsena1.setEstado("Terminado")
            colaTerminados.append(cDarsena1)
            cam = colaDarsena.popleft()
            cam.setEstado("En servidor")
            servidorDarsena1.recibirCamion(cam)
            finAtencionServDar1S = servidorDarsena1.gettiempoFinAtencion()
            cam.setHoraInicioEvento(segundos)
            cam.setHoraFinEvento(servidorDarsena1.gettiempoFinAtencionSegundos())
            atendidosdar1 += 1

            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if (finAtencionServDar1S is not None):
                d2, h2, m2, s2 = finAtencionServDar1S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            stringProxCamion = str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Fin atencion Darsena 1", cDarsena1.getnroCamion(), d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", False)
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados

        if (isinstance(cDarsena2, Camion) and not servidorDarsena2.getCalibrando()):
            cDarsena2.setEstado("En cola")
            finAtencionServDar2S = None
            cDarsena2.setHoraSalida(segundos)
            cDarsena2.setEstado("Terminado")
            colaTerminados.append(cDarsena2)
            cam = colaDarsena.popleft()
            cam.setEstado("En servidor")
            servidorDarsena2.recibirCamion(cam)
            finAtencionServDar2S = servidorDarsena1.gettiempoFinAtencion()
            cam.setHoraInicioEvento(segundos)
            cam.setHoraFinEvento(servidorDarsena1.gettiempoFinAtencionSegundos())
            atendidosdar2 += 1

            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            if (finAtencionServDar2S is not None):
                d2, h2, m2, s2 = finAtencionServDar2S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            stringProxCamion =  str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Fin atencion Darsena 2", cDarsena2.getnroCamion(), d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s")
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados
    else:
        if (isinstance(cDarsena1, Camion) and not servidorDarsena1.getCalibrando()):
            cDarsena1.setEstado("En cola")
            finAtencionServDar1S = None
            cDarsena1.setHoraSalida(segundos)
            cDarsena1.setEstado("Terminado")
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
            stringProxCamion =  str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Fin atencion Darsena 1", cDarsena1.getnroCamion(), d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", False)
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados

        if (isinstance(cDarsena2, Camion) and not servidorDarsena2.getCalibrando()):
            cDarsena2.setEstado("En cola")
            finAtencionServDar2S = None
            cDarsena2.setEstado("Terminado")
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
            stringProxCamion =  str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Fin atencion Darsena 2", cDarsena2.getnroCamion(), d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s")
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados

    if (cDarsena1 is not None and not isinstance(cDarsena1, Camion)):
        if (cDarsena1):
            #empezo calibrado
            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            finAtencionServDar1S = servidorDarsena1.gettiempoFinAtencion()
            if (finAtencionServDar1S is not None):
                d2, h2, m2, s2 = finAtencionServDar1S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            stringProxCamion =  str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Calibrando Darsena 1", "----", d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", False)
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados
        else:
            #termino calibrado
            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            finAtencionServDar1S = servidorDarsena1.gettiempoFinAtencion()
            if (finAtencionServDar1S is not None):
                d2, h2, m2, s2 = finAtencionServDar1S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            stringProxCamion =  str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Fin calibracion Darsena 1", "----", d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s", False)
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados

    if (cDarsena2 is not None and not isinstance(cDarsena2, Camion)):
        if (cDarsena2):
            #empieza calibrado
            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            finAtencionServDar2S = servidorDarsena2.gettiempoFinAtencion()
            if (finAtencionServDar2S is not None):
                d2, h2, m2, s2 = finAtencionServDar2S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            stringProxCamion =  str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Calibrando Darsena 2", "----", d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s")
            r = procesarCamiones(r)
            # fin generacion vector de estados
        else:
            #termina calibrado
            # generacion vector de estados
            d3, h3, m3, s3 = convert_timedelta(proximoCamionS)
            finAtencionServDar2S = servidorDarsena2.gettiempoFinAtencion()
            if (finAtencionServDar2S is not None):
                d2, h2, m2, s2 = finAtencionServDar2S
            else:
                h2 = ".."
                m2 = ".."
                s2 = ".."
            stringProxCamion = str(h3) + "hs " + str(m3) + "min " + str(s3) + "s"
            r = generarVectorDeEstados("Fin calibracion Darsena 2", "----", d, h, m, s, stringProxCamion,
                                       True, True, True,
                                       False, False, False, str(h2) + "hs " + str(m2) + "min " + str(s2) + "s")
            r = procesarCamiones(r)
            vectorEstados.append(r)
            # fin generacion vector de estados

    if (not servidorDarsena1.getOcupado()):
        if (len(colaDarsena) > 0 and not servidorDarsena1.getCalibrando()):
            cam = colaDarsena.popleft()
            cam.setEstado("En servidor")
            servidorDarsena1.recibirCamion(cam)
            cam.setHoraInicioEvento(segundos)
            cam.setHoraFinEvento(servidorDarsena1.gettiempoFinAtencionSegundos())
            atendidosdar1 += 1

    if (not servidorDarsena2.getOcupado()):
        if (len(colaDarsena) > 0 and not servidorDarsena2.getCalibrando()):
            cam = colaDarsena.popleft()
            cam.setEstado("En servidor")
            servidorDarsena2.recibirCamion(cam)
            cam.setHoraInicioEvento(segundos)
            cam.setHoraFinEvento(servidorDarsena2.gettiempoFinAtencionSegundos())
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