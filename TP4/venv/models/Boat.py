import random

# G = GOLPEADO
# E = ERRADO
# O = OCUPADO
# L = LIBRE
# H = HUNDIDO
STATES = ["G", "E", "O", "L"]
state_colors = [(255, 0, 0), (0, 0, 0), (128, 128, 128), (0, 0, 131)]


class Boat:
    x = 0
    y = 0

    def __init__(self, vertical, size, x = 0, y = 0, STATE = []):
        self.vertical = vertical
        self.size = size
        self.x = x
        self.y = y
        self.STATE = ['O'] * size

    def get_cell(self, board):
        i = 0
        while i < self.size:
            if self.vertical:
                board[(self.x, self.y + i)] = state_colors[STATES.index(self.STATE[i])]
            else:
                board[(self.x + i, self.y)] = state_colors[STATES.index(self.STATE[i])]
            i += 1
        return board

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def recibir_ataque(self, x, y):
        hit = False
        hit_index = 0

        if self.vertical:
            if self.x != x:
                return "E"
            if self.y <= y < self.y + self.size:
                hit = True
                hit_index = y - self.y
            else:
                return "E"
        else:
            if self.y != y:
                return "E"
            if self.x <= x < self.x + self.size:
                hit = True
                hit_index = x - self.x
            else:
                return "E"

        if hit:
            self.STATE[hit_index] = "G"
            for s in self.STATE:
                if s != "G":
                    return "G"
            return "H"
