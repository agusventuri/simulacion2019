from random import *


class MixedCongruentialGenerator:

    def __init__(self, seed, m, a, c):
        self.seed = seed
        self.m = m
        self.a = a
        self.c = c

    def generate_number(self):
        random = (self.a * self.seed + self.c) % self.m

        self.seed = random

        return round((random / self.m), 4)

    def generate(self, quantity):
        generated = []

        for i in range(0, quantity):
            generated.append(self.generate_number())

        return generated


class PythonRandomGenerator:
    def generate(self, quantity):
        generated = []

        for i in range(0, quantity):
            x = round(uniform(0, 1), 4)
            generated.append(x)

        return generated


class MultiplicativeCongruentialGenerator:

    def __init__(self, seed, m, a):
        self.seed = seed
        self.m = m
        self.a = a

    def generate_number(self):
        random = (self.a * self.seed) % self.m

        self.seed = random

        return round((random / self.m), 4)


class TestChiCuadrado:
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
