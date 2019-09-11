import random
from abc import ABCMeta, abstractmethod


class IStrategy:
    __metaclass__ = ABCMeta

    @abstractmethod
    def obtener_siguiente_ataque(self): raise NotImplementedError

    @abstractmethod
    def recibir_resultado(self, result): raise NotImplementedError

    @abstractmethod
    def get_hits(self): raise NotImplementedError

    @abstractmethod
    def get_misses(self): raise NotImplementedError


class RandomStrategy(IStrategy):
    not_attacked = {}
    hits = 0
    misses = 0

    def __init__(self):
        for y in range(0, 100):
            for x in range(0, 100):
                self.not_attacked[(x, y)] = None

    def obtener_siguiente_ataque(self):
        try:
            x, y = random.choice(list(self.not_attacked.keys()))
            del self.not_attacked[(x, y)]
        except IndexError:
            return 0, 0
        return x, y

    def recibir_resultado(self, result):
        if result == "G" or result == "H":
            self.hits += 1
        if result == "E":
            self.misses += 1

    def get_hits(self):
        return self.hits

    def get_misses(self):
        return self.misses


class HuntAndTargetStrategy(IStrategy):
    attacked = {}
    not_attacked = {}
    hits = 0
    misses = 0

    def __init__(self):
        self.attack_buffer = {}
        self.last_x_attacked = None
        self.last_y_attacked = None
        for y in range(0, 100):
            for x in range(0, 100):
                if (x + y + 100 % 2 + 1) % 2:
                    self.not_attacked[(x, y)] = None

    def obtener_siguiente_ataque(self):
        if len(self.attack_buffer) != 0:
            x, y = random.choice(list(self.attack_buffer.keys()))
            del self.attack_buffer[(x, y)]
            try:
                del self.not_attacked[(x, y)]
            except: pass
            self.attacked[(x, y)] = None
            self.last_y_attacked = y
            self.last_x_attacked = x
            return x, y

        try:
            x, y = random.choice(list(self.not_attacked.keys()))
            del self.not_attacked[(x, y)]
            self.attacked[(x, y)] = None
        except IndexError:
            self.last_y_attacked = 0
            self.last_x_attacked = 0
            return 0, 0
        self.last_y_attacked = y
        self.last_x_attacked = x
        return x, y

    def recibir_resultado(self, result):
        if result == "G" or result == "H":
            self.hits += 1
            # si la celda adyacente no fue atacada aún y tampoco está en el buffer de ataque la agregamos al buffer
            # y la quitamos de la lista de no atacados
            # definimos celdas adyacentes
            x1 = (self.last_x_attacked + 1, self.last_y_attacked)
            x2 = (self.last_x_attacked - 1, self.last_y_attacked)
            y1 = (self.last_x_attacked, self.last_y_attacked + 1)
            y2 = (self.last_x_attacked, self.last_y_attacked - 1)

            if x1 not in self.attacked and x1 not in self.attack_buffer and x1[0] < 100:
                self.attack_buffer[x1] = None

            if x2 not in self.attacked and x2 not in self.attack_buffer and x2[0] >= 0:
                self.attack_buffer[x2] = None

            if y1 not in self.attacked and y1 not in self.attack_buffer and y1[1] < 100:
                self.attack_buffer[y1] = None

            if y2 not in self.attacked and y2 not in self.attack_buffer and y2[1] >= 0:
                self.attack_buffer[y2] = None
        if result == "E":
            self.misses += 1

    def get_hits(self):
        return self.hits

    def get_misses(self):
        return self.misses
