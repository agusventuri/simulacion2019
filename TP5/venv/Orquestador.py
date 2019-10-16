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

def obtenerTiempoProxCamion():
    #formula gen var aleatoria exponencial
    t = (-unoSobreLambda) * math.log(1 - random.random(),math.e)
    #t=15
    t=round((t),0)
    #global tiempolleg
    #tiempolleg=t

    return t

# tiempo en segundos hasta la llegada del proximo camion
proximoCamion = obtenerTiempoProxCamion()

while dia <= 30:
    #si sale el ultimo camion se termina d trabajar y se pasa al otro dia

    #control del tiempo
    if (segundos!=0 and segundos % 3600 == 0):
        hora += 1
        # permitir llegada de camiones
        if (hora >= 12 and hora <= 18):
            flagLleganCamiones = True
        else:
            flagLleganCamiones = False

        # permitir atencion de camiones
        #if (hora >= 5):
        #    flagPuertasAbiertas = True

        # almacenar la cantidad de camiones que duermen afuera
        if (hora >= 18):
           cantidadDuermenAfuera[dia-1]= len(colaRecepcion)

        # permitir recepcion de camiones
        if (hora >= 5 and hora <= 18):
            flagRecibirCamiones = True
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

    #si esta entre las 12 y las 18, siguen llegando camiones
    if (flagLleganCamiones):

        if (proximoCamion > 0):
            proximoCamion -= 1
        else:
            colaRecepcion.append(Camion(random.random() < 0.35))
            agregadosColaRecepcion+=1
            proximoCamion = obtenerTiempoProxCamion()
    else:
        proximoCamion = obtenerTiempoProxCamion()

    #print("---------------")
    #print("prox camion" + str(proximoCamion))

    # si recepcion esta atendiendo a alguien lo sigue atendiendo, pero no recibe camiones pasadas las 18hs
    if (flagRecibirCamiones):
        c = servidorRecepcion.obtenerEvento()
        if (c is not None):
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
                    atendidosrec += 1

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
        colaDarsena.append(cBalanza)
        if(len(colaBalanza) > 0):
            servidorBalanza.recibirCamion(colaBalanza.popleft())
            atendidosbal += 1


    if (not servidorBalanza.getOcupado()):
        if (len(colaBalanza) > 0):
            servidorBalanza.recibirCamion(colaBalanza.popleft())
            atendidosbal += 1

    #servidores darsena
    cDarsena1 = servidorDarsena1.obtenerEvento()
    cDarsena2 = servidorDarsena2.obtenerEvento()
    #ver a que darsena le tengo q pasar un camion
    if (len(colaDarsena)>0):
        if (isinstance(cDarsena1, Camion)):
            cDarsena1.setHoraSalida(segundos)
            colaTerminados.append(cDarsena1)
            servidorDarsena1.recibirCamion(colaDarsena.popleft())
            atendidosdar1 += 1

        if (isinstance(cDarsena2, Camion)):
            cDarsena2.setHoraSalida(segundos)
            colaTerminados.append(cDarsena2)
            servidorDarsena2.recibirCamion(colaDarsena.popleft())
            atendidosdar2 += 1
    else:
        if (isinstance(cDarsena1, Camion)):
            cDarsena1.setHoraSalida(segundos)
            colaTerminados.append(cDarsena1)
            atendidosdar1 += 1
        if (isinstance(cDarsena2, Camion)):
            colaTerminados.append(cDarsena2)
            cDarsena2.setHoraSalida(segundos)
            atendidosdar2 += 1


    if (not servidorDarsena1.getOcupado()):
        if (len(colaDarsena) > 0):
            servidorDarsena1.recibirCamion(colaDarsena.popleft())
            atendidosdar1 += 1

    if (not servidorDarsena2.getOcupado()):
        if (len(colaDarsena) > 0):
            servidorDarsena2.recibirCamion(colaDarsena.popleft())
            atendidosdar2 += 1

    #if hora==16 and proximoCamion<=1 and ((servidorRecepcion.gettiempoFinAtencion()<=8 and servidorRecepcion.gettiempoFinAtencion()!=0) or (servidorBalanza.gettiempoFinAtencion()<=10 and servidorBalanza.gettiempoFinAtencion()!=0) or (servidorDarsena1.gettiempoFinAtencion()<=10 and servidorDarsena1.gettiempoFinAtencion()!=0)or (servidorDarsena2.gettiempoFinAtencion()<=10 and servidorDarsena2.gettiempoFinAtencion()!=0)):
    #    time.sleep(0)

    #print("---------------------------")
    #print("Dia:" + str(dia) + "Hora:"+ str(hora)+ "segundos: "+ str(segundos))
    #print("serv recepcion")
    #if servidorRecepcion.camion is not None:
    #    print("atendiendo camion : "+str(servidorRecepcion.camion.getnroCamion()) + " prox fin atencion: "+ str(servidorRecepcion.gettiempoFinAtencion()))
    #print("serv Balanza")
    #if servidorBalanza.camion is not None:
    #    print("atendiendo camion : "+str(servidorBalanza.camion.getnroCamion())+  " prox fin atencion: "+str(servidorBalanza.gettiempoFinAtencion()))
    #print("serv darsena1" +" cantidad recalibrados: "+str(servidorDarsena1.getRecalibrados()))
    #if servidorDarsena1.camion is not None:
    #    print("atendiendo camion : "+str(servidorDarsena1.camion.getnroCamion())+ " prox fin atencion: "+ str(servidorDarsena1.gettiempoFinAtencion()))
    #print("serv darsena2" +" cantidad recalibrados: "+str(servidorDarsena2.getRecalibrados()))
    #if servidorDarsena2.camion is not None:
    #    print("atendiendo camion : "+str(servidorDarsena2.camion.getnroCamion())+  " prox fin atencion: "+str(servidorDarsena2.gettiempoFinAtencion()))
    #print("colas:")
    #print(len(colaRecepcion))
    #print(len(colaBalanza))
    #print(len(colaDarsena))
    #print("cantidad atendidos:")
    #print(atendidosrec)
    #print(atendidosbal)
    #print(atendidosdar1)
    #print(atendidosdar2)
    #print("agregados a colas:")
    #print(agregadosColaRecepcion)
    #print(agregadosColaBalanza)
    #print(agregadosColaDar)

    #print("proximo camion"+str(proximoCamion))

    #print("tiempos de atencion generados: ")
    #print("prox camion epec : "+str(tiempolleg))

    #print(str(cantidadDuermenAfuera))
    segundos += 1

def convert_timedelta(seconds):
    duration = datetime.timedelta(seconds=seconds)
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds

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


#print("Tiempo promedio permanencia: "+str(tiempoPromedioCamiones))
#print(len(colaTerminados))
#print(cantidadDuermenAfuera)
#print(cantidadAtendidos)

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

print("Listo")

os.system('python Orquestador2daEstrategia.py')
