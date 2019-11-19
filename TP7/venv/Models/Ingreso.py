from datetime import datetime
from datetime import timedelta

class Ingreso():
    def __init__(self, distribucionIngreso):
        self.distribucion = distribucionIngreso
        self.proximaLlegada = datetime(1, 1, 1, hour=0, minute=0, second=0)

    def actualizarIngreso(self):
        demora = round(self.distribucion.generar() * 60, 0)
        self.proximaLlegada = self.proximaLlegada + timedelta(seconds = demora)
