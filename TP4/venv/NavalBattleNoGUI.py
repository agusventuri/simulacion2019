import random
import sys
from models.Boat import Boat
from models.Jugador import Jugador
from models.Strategy import RandomStrategy
from models.Strategy import HuntAndTargetStrategy

# SHAPE FORMATS
# G = "GOLPEADO"
# E = "ERRADO"
# O = "OCUPADO"
# L = "LIBRE"

strategy_random = RandomStrategy()
strategy_parity_hunt = HuntAndTargetStrategy()

jugador_random = Jugador(strategy_random)
jugador_hunt = Jugador(strategy_parity_hunt)


def automatic(simulations_number):
    global jugador_random, jugador_hunt, strategy_random, strategy_parity_hunt

    run = simulations_number

    cantidad_wins_random = 0
    cantidad_wins_hunt_and_target = 0
    cantidad_misses_random = 0
    cantidad_hits_random = 0
    cantidad_misses_hunt = 0
    cantidad_hits_hunt = 0
    cantidad_barcos_perdidos_j1 = 0
    cantidad_barcos_perdidos_j2 = 0

    while run > 0:
        x, y = jugador_hunt.atacar()
        result1 = jugador_random.recibir_ataque(x, y)
        jugador_hunt.recibir_resultado(result1)

        if result1 == "L":
            cantidad_wins_random += 1
            cantidad_misses_random += jugador_random.get_misses()
            cantidad_hits_random += jugador_random.get_hits()
            cantidad_misses_hunt += jugador_hunt.get_misses()
            cantidad_hits_hunt += jugador_hunt.get_hits()
            cantidad_barcos_perdidos_j1 += jugador_hunt.get_barcos_perdidos()
            cantidad_barcos_perdidos_j2 += jugador_random.get_barcos_perdidos()
            run -= 1
            reset()
            continue

        x, y = jugador_random.atacar()
        result2 = jugador_hunt.recibir_ataque(x, y)
        jugador_random.recibir_resultado(result2)

        if result2 == "L":
            cantidad_wins_hunt_and_target += 1
            cantidad_misses_random += jugador_random.get_misses()
            cantidad_hits_random += jugador_random.get_hits()
            cantidad_misses_hunt += jugador_hunt.get_misses()
            cantidad_hits_hunt += jugador_hunt.get_hits()
            cantidad_barcos_perdidos_j1 += jugador_hunt.get_barcos_perdidos()
            cantidad_barcos_perdidos_j2 += jugador_random.get_barcos_perdidos()
            run -= 1
            reset()
            continue

    winner = (strategy_parity_hunt.__class__.__name__, strategy_random.__class__.__name__)[
        cantidad_wins_random > cantidad_wins_hunt_and_target]
    winner_points = (cantidad_wins_random, cantidad_wins_hunt_and_target)[
        winner == strategy_parity_hunt.__class__.__name__]
    loser = (strategy_random.__class__.__name__, strategy_parity_hunt.__class__.__name__)[
        cantidad_wins_random > cantidad_wins_hunt_and_target]
    loser_points = (cantidad_wins_random, cantidad_wins_hunt_and_target)[
        winner != strategy_parity_hunt.__class__.__name__]
    return cantidad_misses_random, \
           cantidad_hits_random, \
           cantidad_misses_hunt, \
           cantidad_hits_hunt, \
           winner, \
           winner_points, \
           loser, \
           loser_points, \
           cantidad_barcos_perdidos_j1, \
           cantidad_barcos_perdidos_j2


def reset():
    global occupied_positions1, occupied_positions2, jugador_random, jugador_hunt, strategy_random, strategy_parity_hunt
    occupied_positions1 = {}
    occupied_positions2 = {}

    strategy_random = RandomStrategy()
    strategy_parity_hunt = HuntAndTargetStrategy()

    jugador_random = Jugador(strategy_random)
    jugador_hunt = Jugador(strategy_parity_hunt)
