import random
from abc import ABCMeta, abstractmethod


class IServidor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def obtenerEvento(self): raise NotImplementedError


class Recepcion(IServidor):

    def __init__(self):
        pass

    def obtenerEvento(self):
        pass


class Balanza(IServidor):

    def __init__(self):
        pass

    def obtenerEvento(self):
        pass


class Darsena(IServidor):

    def __init__(self):
        pass

    def obtenerEvento(self):
        pass