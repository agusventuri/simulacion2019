import random
from abc import ABCMeta, abstractmethod


class IStrategy:
    __metaclass__ = ABCMeta
    attacked = {}
    not_attacked = {}

    @abstractmethod
    def obtener_siguiente_ataque(self): raise NotImplementedError


class RandomStrategy(IStrategy):

    def __init__(self):
        for x in range(0, 99):
            for y in range(0, 99):
                self.not_attacked[(x, y)] = None

    def obtener_siguiente_ataque(self):
        x, y = random.choice(list(self.not_attacked.keys()))
        del self.not_attacked[(x, y)]
        self.attacked[(x, y)] = None
        return x, y


class HuntAndTargetStrategy(IStrategy):

    def obtener_siguiente_ataque(self):
        pass
