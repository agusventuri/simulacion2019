import random
from models.Boat import Boat
from models.Strategy import IStrategy


class Jugador:
    occupied_positions = {}

    def __init__(self, strategy):
        self.barcos = self.crear_barcos()
        self.strategy = strategy
        self.occupied_positions = {}

    def crear_barcos(self):
        # 5 tipos de barco, creo 2 x cada uno
        bar = []
        for i in range(2, 7):
            b = Boat(random.getrandbits(1), i)
            b1 = Boat(random.getrandbits(1), i)
            bar.append(self.posicionar_barco(b))
            bar.append(self.posicionar_barco(b1))

        return bar

    def posicionar_barco(self, barco):
        valida = False

        while not valida:
            x = random.randrange(0, 100)
            y = random.randrange(0, 100)

            if not self.posicionValida(x, y, barco):
                continue
            else:
                barco.set_x(x)
                barco.set_y(y)
                self.occupied_positions[(x, y)] = (128, 128, 128)
                for i in range(1, barco.size):
                    if barco.vertical:
                        self.occupied_positions[(x, y + i)] = (128, 128, 128)
                    else:
                        self.occupied_positions[(x + i, y)] = (128, 128, 128)
                valida = True

        return barco

    def posicionValida(self, x, y, barco):
        # primero chequeo que no exista ya esa entrada
        if (x, y) in self.occupied_positions:
            return False

        # chequeo que el barco no exceda limites del tablero
        if (x + barco.size) >= 100 or (y + barco.size) >= 100:
            return False

        # el barco entra en el tablero
        # ahora me fijo que no haya posiciones ocupadas donde  lo quiero colocar
        if barco.vertical:
            for i in range(barco.size):
                # voy sumando en y
                if (x, y + i) in self.occupied_positions:
                    return False
        else:
            for i in range(barco.size):
            # voy sumando en x
                if (x + i, y) in self.occupied_positions:
                    return False

        return True

    def get_occupied_positions(self):
        for item in self.barcos:
            self.occupied_positions = item.get_cell(self.occupied_positions)
        return self.occupied_positions

    def recibir_ataque(self, x, y):
        result = "E"

        for barco in self.barcos:
            result = barco.recibir_ataque(x, y)
            if result is not "E":
                break

        if result is "E":
            self.occupied_positions[(x, y)] = (0, 0, 0)
        return result

    def atacar(self):
        # esta funcion debe devolver un par x o y segun la estrategia usada
        x, y = self.strategy.obtener_siguiente_ataque()
        return x, y
