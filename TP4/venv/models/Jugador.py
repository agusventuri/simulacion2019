import random
from models.Boat import Boat
from models.Strategy import IStrategy


class Jugador:

    def __init__(self, strategy):
        self.strategy = strategy
        self.occupied_positions = {}
        self.boats_positions = {}
        self.atacado = True
        self.barcos = []
        self.barcos = self.crear_barcos()

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

            if not self.posicion_valida(x, y, barco):
                continue
            else:
                barco.set_x(x)
                barco.set_y(y)
                self.boats_positions[(x, y)] = None
                self.occupied_positions[(x, y)] = (128, 128, 128)
                for i in range(1, barco.size):
                    if barco.vertical:
                        self.occupied_positions[(x, y + i)] = (128, 128, 128)
                        self.boats_positions[(x, y + i)] = None
                    else:
                        self.occupied_positions[(x + i, y)] = (128, 128, 128)
                        self.boats_positions[(x + i, y)] = None
                valida = True

        return barco

    def posicion_valida(self, x, y, barco):
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
        return self.occupied_positions

    def recibir_ataque(self, x, y):
        if len(self.boats_positions) == 0:
            return "L"

        if (x, y) not in self.boats_positions:
            self.occupied_positions[(x, y)] = (0, 0, 0)
            return "E"

        for barco in self.barcos:
            self.atacado = True
            result = barco.recibir_ataque(x, y)
            if result is "G" or result is "H":
                self.occupied_positions = barco.get_cell(self.occupied_positions)
                del self.boats_positions[x, y]
                return result

    def atacar(self):
        # esta funcion debe devolver un par x o y segun la estrategia usada
        x, y = self.strategy.obtener_siguiente_ataque()
        return x, y

    def recibir_resultado(self, result):
        self.strategy.recibir_resultado(result)

    def get_hits(self):
        return self.strategy.get_hits()

    def get_misses(self):
        return self.strategy.get_misses()
