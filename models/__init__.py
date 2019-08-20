from random import *


# Generador de Número Aleatorios mediante Método Congruencial Mixto.
class MixedCongruentialGenerator:

    # Constructor. Inicialización de las variable necesarias para generar los números.
    def __init__(self, seed, m, a, c):
        self.seed = seed
        self.m = m
        self.a = a
        self.c = c

    # Método que genera un único número aleatorio mediante el método congruencial mixto basado en las variables de
    # inicialización.
    def generate_number(self):
        random = (self.a * self.seed + self.c) % self.m

        self.seed = random

        return round((random / self.m), 4)

    # Método que genera n números aleatorios mediante el método congruencial mixto basado en las variables de
    # inicialización. La cantidad de números esta dada por el parámetro quantity.
    def generate(self, quantity):
        generated = []

        for i in range(0, quantity):
            generated.append(self.generate_number())

        return generated


# Generador de Número Aleatorios mediante el método provisto por el lenguaje.
class PythonRandomGenerator:

    # Método que genera n números aleatorios mediante el método provisto por el lenguaje. La cantidad de números esta
    # dada por el parámetro quantity.
    @staticmethod
    def generate(quantity):
        generated = []

        for i in range(0, quantity):
            x = round(uniform(0, 1), 4)
            generated.append(x)

        return generated

    # Método que genera un único número aleatorio mediante el método provisto por el lenguaje.
    @staticmethod
    def generate_number():
        return round(uniform(0, 1), 4)


# Generador de Número Aleatorios mediante Método Congruencial Multiplicativo.
class MultiplicativeCongruentialGenerator:

    # Constructor. Inicialización de las variable necesarias para generar los números.
    def __init__(self, seed, m, a):
        self.seed = seed
        self.m = m
        self.a = a

    # Método que genera un único número aleatorio mediante el método congruencial multiplicativo basado en las variables
    # de inicialización.
    def generate_number(self):
        random = (self.a * self.seed) % self.m

        self.seed = random

        return round((random / self.m), 4)

    # Método que genera n números aleatorios mediante el método congruencial multiplicativo basado en las variables de
    # inicialización. La cantidad de números esta dada por el parámetro quantity.
    def generate(self, quantity):
        generated = []

        for i in range(0, quantity):
            generated.append(self.generate_number())

        return generated


# Ejecutor del Test de Chi Cuadrado.
class TestChiCuadrado:

    # Método encargado de crear n intervalos (definidos por el parámetro quantity), entre un valor máximo y mínimo.
    # Por defecto el máximo es 1 y el mínimo 0, pero pueden ser modificados mediante los parámetro min y max
    @staticmethod
    def divide_intervals(quantity, max=1, min=0):
        step = (max - min) / quantity
        intervals = []
        average = []

        i = 0
        while i < quantity:
            if i == 0:
                intervals.append([round(min, 4), round(min + step, 4)])
            else:
                lastMinimum = round(intervals[i - 1][1], 4)
                intervals.append([lastMinimum, round(lastMinimum + step, 4)])

            i += 1

        for i in intervals:
            average.append(round((i[0] + i[1]) / 2, 4))

        return intervals, average

    # Ejecuta el test de chi cuadrado sobre una serie de números, contra una serie de intervalos.
    #
    # El parámetro series debe ser una lista con los números a quien se quiere realizar la prueba.
    #
    # El parámetro intervals debe ser una lista de tuplas de la forma [[n_min, n_max], ..., [n_min, n_max]] contra la
    # cual se comparar la serie.
    #
    # Se retornan dos listas, una con la frecuencia esperada y otra con la frecuencia real de los número de la serie
    # para los intervalos dados.
    @staticmethod
    def test_chi_cuadrado(series, intervals):
        intervals_quantity = len(intervals)
        expected_frequency = [int(len(series) / intervals_quantity)] * len(intervals)
        real_frequency = []

        for i in intervals:
            appearance = 0

            for item in series:
                if i[0] <= item < i[1]:
                    appearance += 1

            real_frequency.append(appearance)

        return expected_frequency, real_frequency

    # Genera una serie de números para una frecuencia esperada.
    #
    # El parámetro average debe ser una lista de los valores de la media de cada intervalo.
    #
    # TODO: Modificar expected_distribution_interval para que pueda ser una lista con el valor esperado de cada
    #  intervalo.
    # El parámetro expected_distribution_interval es el valor de la distribución esperada.
    #
    # min_value y max_value corresponden a los valores mínimos y máximos que la serie puede tener.
    @staticmethod
    def generate_expected_distribution(averages, expected_distribution_interval, min_value, max_value):
        expected = []

        for a in averages:
            for n in range(0, expected_distribution_interval):
                expected.append(a)

        expected.pop(0)
        expected.pop()

        expected.append(min_value - min_value)
        expected.append(max_value)

        return expected
