import random
import math
from abc import ABCMeta, abstractmethod

class IDistribucion:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generar(self): raise NotImplementedError


class DistribucionUniforme(IDistribucion):

    def __init__(self, a, b):
        self.A = a
        self.B = b

    def generar(self):
        rnd = random.random()
        return self.A + (rnd * (self.B - self.A))


class DistribucionExponencialNegativa(IDistribucion):
    def __init__(self, Lambda):
        self.Lambda = Lambda

    def generar(self):
        rnd = random.random()
        return (-self.Lambda) * math.log(1 - rnd)


class DistribucionNormal(IDistribucion):
    def __init__(self, media, varianza):
        self.media = media
        self.varianza = varianza

    def generar(self):
        rnd1 = random.random()
        rnd2 = rnd1 + 1

        z = math.sqrt((-2) * math.log(rnd1)) * math.cos(2 * math.pi * rnd2)

        return (self.media + (z * self.varianza))


class DiffUnTrabajo(IDistribucion):
    def __init__(self):
        pass

    def generar(self, mojado):
        v1 = mojado
        h = 0.0001
        t = 0.0

        v1Prima = (-0.5 * mojado) - 0.04 + (0.0001 * t)

        while (v1 >= 1):
            t += h
            v1 += h * v1Prima
            v1Prima = (-0.5 * v1) - 0.04 + (0.0001 * t)

        return t


class DiffDosTrabajo(IDistribucion):
    def __init__(self):
        pass

    def generar(self, mojado):
        v1 = mojado
        h = 0.0001
        t = 0.0

        v1Prima = (-0.5 * mojado) + 0.04 + (0.0001 * t)

        while (v1 >= 1):
            t += h
            v1 += h * v1Prima
            v1Prima = (-0.5 * v1) + 0.04 + (0.0001 * t)

        return t