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
        for y in range(0, 100):
            for x in range(0, 100):
                self.not_attacked[(x, y)] = None
        print(self.not_attacked)

    def obtener_siguiente_ataque(self):
        #x, y = random.choice(list(self.not_attacked.keys()))
        x, y = self.not_attacked.popitem()[0]
        #del self.not_attacked[(x, y)]
        self.attacked[(x, y)] = None
        return x, y


class HuntAndTargetStrategy(IStrategy):

    def obtener_siguiente_ataque(self):
        pass
