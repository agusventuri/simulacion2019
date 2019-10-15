from Models.Camion import Camion
from Models.Servidor import Recepcion
from Models.Servidor import Balanza
from Models.Servidor import Darsena
from collections import deque
import math
import random
import time

# creamos deques. Con append agregamos a la derecha, y con popleft sacamos desde la izquierda
colaRecepcion = deque()
colaBalanza = deque()
colaDarsena = deque()

dia = 1
hora = 4
segundos = 18000
lambdallegadas = 7.5 # 7,5 minutos
cantidadDuermenAfuera = [0]*30

servidorRecepcion = Recepcion()
servidorBalanza = Balanza()
servidorDarsena1 = Darsena()
servidorDarsena2 = Darsena()
atendidosrec=0
atendidosbal=0
atendidosdar1=0
atendidosdar2=0




# bandera que permite la llegada de camiones (entre las 12 hs y las 18)
flagLleganCamiones = False
flagPuertasAbiertas = False
flagRecibirCamiones = False

def obtenerTiempoProxCamion():
    #formula gen var aleatoria exponencial
    t = (-1 / lambdallegadas) * math.log(1 - random.random(),math.e)
    #t=15
    t=round((t*60),0)

    return t

# tiempo en segundos hasta la llegada del proximo camion
proximoCamion = obtenerTiempoProxCamion()

while dia <= 30:
    if dia==1 and hora==16:
        print("segundos: "+ str(segundos))
        exit()

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
        if (hora >= 5):
            flagPuertasAbiertas = True

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
            hora = 0
            dia += 1

    #si esta entre las 12 y las 18, siguen llegando camiones
    if (flagLleganCamiones):

        if (proximoCamion > 0):
            proximoCamion -= 1
        else:
            colaRecepcion.append(Camion(segundos, random.random() > 0.35))
            proximoCamion = obtenerTiempoProxCamion()
    else:
        proximoCamion = obtenerTiempoProxCamion()

    print("---------------")
    print("prox camion" + str(proximoCamion))

    # si recepcion esta atendiendo a alguien lo sigue atendiendo, pero no recibe camiones pasadas las 18hs
    c = servidorRecepcion.obtenerEvento()
    if (c is not None):
        if (c.getPropio()):
            colaDarsena.append(c)
        else:
            colaBalanza.append(c)
        if(len(colaRecepcion) > 0):
            if (flagRecibirCamiones):
                servidorRecepcion.recibirCamion(colaRecepcion.popleft())
                atendidosrec += 1

    if (not servidorRecepcion.getOcupado()):
         if (len(colaRecepcion) > 0):
             servidorRecepcion.recibirCamion(colaRecepcion.popleft())
             atendidosrec += 1

    #servidor balanza
    cBalanza = servidorBalanza.obtenerEvento()
    if (cBalanza is not None):
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
        if (cDarsena1 is not None):
            servidorDarsena1.recibirCamion(colaDarsena.popleft())
            atendidosdar1 += 1

        if (cDarsena2 is not None):
            servidorDarsena2.recibirCamion(colaDarsena.popleft())
            atendidosdar2 += 1

    if (not servidorDarsena1.getOcupado()):
        if (len(colaDarsena) > 0):
            servidorDarsena1.recibirCamion(colaDarsena.popleft())
            atendidosdar1 += 1

    if (not servidorDarsena2.getOcupado()):
        if (len(colaDarsena) > 0):
            servidorDarsena2.recibirCamion(colaDarsena.popleft())
            atendidosdar2 += 1



    if hora==12 and proximoCamion<=1 and ((servidorRecepcion.gettiempoFinAtencion()<=8 and servidorRecepcion.gettiempoFinAtencion()!=0) or (servidorBalanza.gettiempoFinAtencion()<=10 and servidorBalanza.gettiempoFinAtencion()!=0) or (servidorDarsena1.gettiempoFinAtencion()<=10 and servidorDarsena1.gettiempoFinAtencion()!=0)or (servidorDarsena2.gettiempoFinAtencion()<=10 and servidorDarsena2.gettiempoFinAtencion()!=0)):
        time.sleep(10)

    print("---------------------------")
    print("Dia:" + str(dia) + "Hora:"+ str(hora)+ "segundos: "+ str(segundos))
    print("serv recepcion")
    if servidorRecepcion.camion is not None:
        print("atendiendo camion : "+str(servidorRecepcion.camion.getnroCamion()) + " prox fin atencion: "+ str(servidorRecepcion.gettiempoFinAtencion()))
    print("serv Balanza")
    if servidorBalanza.camion is not None:
        print("atendiendo camion : "+str(servidorBalanza.camion.getnroCamion())+  " prox fin atencion: "+str(servidorBalanza.gettiempoFinAtencion()))
    print("serv darsena1")
    if servidorDarsena1.camion is not None:
        print("atendiendo camion : "+str(servidorDarsena1.camion.getnroCamion())+ " prox fin atencion: "+ str(servidorDarsena1.gettiempoFinAtencion()))
    print("serv darsena2")
    if servidorDarsena2.camion is not None:
        print("atendiendo camion : "+str(servidorDarsena2.camion.getnroCamion())+  " prox fin atencion: "+str(servidorDarsena2.gettiempoFinAtencion()))
    print("colas:")
    print(len(colaRecepcion))
    print(len(colaBalanza))
    print(len(colaDarsena))
    print("cantidad atendidos:")
    print(atendidosrec)
    print(atendidosbal)
    print(atendidosdar1)
    print(atendidosdar2)

    segundos += 1

