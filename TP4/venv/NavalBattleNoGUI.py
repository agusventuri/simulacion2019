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


def main():
    global jugador_random, jugador_hunt, strategy_random, strategy_parity_hunt

    run = 10

    cantidad_wins_random = 0
    cantidad_wins_hunt_and_target = 0

    while run > 0:
        x, y = jugador_hunt.atacar()
        result1 = jugador_random.recibir_ataque(x, y)
        jugador_hunt.recibir_resultado(result1)

        if result1 == "L":
            cantidad_wins_random += 1
            run -= 1
            reset()
            continue

        x, y = jugador_random.atacar()
        result2 = jugador_hunt.recibir_ataque(x, y)
        jugador_random.recibir_resultado(result2)

        if result2 == "L":
            cantidad_wins_hunt_and_target += 1
            run -= 1
            reset()
            continue

    winner = (strategy_parity_hunt.__class__.__name__, strategy_random.__class__.__name__)[cantidad_wins_random > cantidad_wins_hunt_and_target]
    winnerPoints = (cantidad_wins_random, cantidad_wins_hunt_and_target)[winner == strategy_parity_hunt.__class__.__name__]
    loser = (strategy_random.__class__.__name__, strategy_parity_hunt.__class__.__name__)[cantidad_wins_random > cantidad_wins_hunt_and_target]
    loserPoints = (cantidad_wins_random, cantidad_wins_hunt_and_target)[winner != strategy_parity_hunt.__class__.__name__]
    print("La estrategia ganadora es " + winner + " con " + str(winnerPoints) + " partidas ganadas.")
    print("La estrategia perdedora es " + loser + " con " + str(loserPoints) + " partidas ganadas.")


def reset():
    global occupied_positions1, occupied_positions2, jugador_random, jugador_hunt, strategy_random, strategy_parity_hunt
    occupied_positions1 = {}
    occupied_positions2 = {}

    strategy_random = RandomStrategy()
    strategy_parity_hunt = HuntAndTargetStrategy()

    jugador_random = Jugador(strategy_random)
    jugador_hunt = Jugador(strategy_parity_hunt)


reset()
main()  # start game
