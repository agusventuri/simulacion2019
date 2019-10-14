from Models.Camion import Camion
from Models.Servidor import Recepcion
from Models.Servidor import Balanza
from Models.Servidor import Darsena
from collections import deque
import random

# creamos deques. Con append agregamos a la derecha, y con popleft sacamos desde la izquierda
colaRecepcion = deque()
colaBalanza = deque()
colaDarsena = deque()

dia = 1
hora = 0
segundos = 0

servidorRecepcion = Recepcion()
servidorBalanza = Balanza()
servidorDarsena1 = Darsena()
servidorDarsena2 = Darsena()

def obtenerTiempoProxCamion():
    return random.randrange(90, 420)

# tiempo en segundos hasta la llegada del proximo camion
proximoCamion = obtenerTiempoProxCamion()

while dia <= 30:
    segundos += 1

    if (proximoCamion != 0):
        proximoCamion -= 1
    else:
        colaRecepcion.append(Camion(segundos, random.random() > 0.35))
        proximoCamion = obtenerTiempoProxCamion()

        # TODO: Pasar camion al servidor de recepcion o a la cola de recepcion

    c = servidorRecepcion.obtenerEvento()
    if (c is not None):
        if (c.getPropio()):
            colaDarsena.append(c)
        else:
            colaBalanza.append(c)
        if(len(colaRecepcion) > 0):
            servidorRecepcion.recibirCamion(colaRecepcion.popleft())
            
        print("---------------------------")
        print(len(colaRecepcion))
        print(len(colaBalanza))
        print(len(colaDarsena))

    if (not servidorRecepcion.getOcupado()):
        if (len(colaRecepcion) > 0):
            servidorRecepcion.recibirCamion(colaRecepcion.popleft())

    if (segundos % 3600 == 0):
        hora += 1
        if (hora == 24):
            hora = 0
            dia += 1