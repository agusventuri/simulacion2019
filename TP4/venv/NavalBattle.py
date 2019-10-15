import pygame
import random
import sys
import time
from models.Boat import Boat
from models.Jugador import Jugador
from models.Strategy import RandomStrategy
from models.Strategy import HuntAndTargetStrategy
import NavalBattleNoGUI as noGui

# from models import Strategy

pygame.font.init()

# GLOBALS VARS
number_of_simulations = 10
s_width = 1300
s_height = 700
play_width = 600  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 6
y_offset = -40

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
# G = "GOLPEADO"
# E = "ERRADO"
# O = "OCUPADO"
# L = "LIBRE"

STATES = ["G", "E", "O", "L"]
state_colors = [(255, 0, 0), (0, 0, 0), (128, 128, 128), (0, 0, 131)]

occupied_positions1 = {}
occupied_positions2 = {}

strategy_random = RandomStrategy()
strategy_parity_hunt = HuntAndTargetStrategy()

jugador1 = Jugador(strategy_random)
jugador2 = Jugador(strategy_parity_hunt)

grid1 = []
grid2 = []


def create_grid(occupied_positions={}):
    grid = [[(0, 0, 131) for x in range(0, 100)] for x in range(0, 100)]

    for key in occupied_positions:
        grid[key[1]][key[0]] = occupied_positions[key]

    return grid


def draw_grid(surface, row, col):
    sx1 = s_width - 25 - play_width
    sx2 = 25
    sy = top_left_y + y_offset

    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx1, sy + i * block_size),
                         (sx1 + play_width, sy + i * block_size))  # horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (sx2, sy + i * block_size),
                         (sx2 + play_width, sy + i * block_size))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx1 + j * block_size, sy),
                             (sx1 + j * block_size, sy + play_height))  # vertical lines
            pygame.draw.line(surface, (128, 128, 128), (sx2 + j * block_size, sy),
                             (sx2 + j * block_size, sy + play_height))  # vertical lines


def draw_text_middle(text, size, color, surface, y_offset):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    surface.blit(surface, (0, 0))
    surface.fill(pygame.Color("black"))
    offset = 0
    for i in text:
        label = font.render(i, 1, color)
        surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                             top_left_y + (play_height / 2) - (label.get_height() / 2) + offset - 10))
        offset += y_offset


def draw_window(surface):
    global grid1, grid2
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Batalla Naval', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 10))

    sx1 = s_width - 25 - play_width
    sx2 = 25

    for i in range(0, 100):
        for j in range(0, 100):
            pygame.draw.rect(surface, grid1[i][j], (sx1 + j * block_size, top_left_y + i * block_size + y_offset,
                                                    block_size, block_size), 0)

    for o in range(0, 100):
        for k in range(0, 100):
            pygame.draw.rect(surface, grid2[o][k], (sx2 + k * block_size, top_left_y + o * block_size + y_offset,
                                                    block_size, block_size), 0)

    # draw grid and border
    draw_grid(surface, 100, 100)
    pygame.draw.rect(surface, (255, 0, 0), (sx1, top_left_y + y_offset, play_width, play_height), 2)
    pygame.draw.rect(surface, (255, 0, 0), (sx2, top_left_y + y_offset, play_width, play_height), 2)
    # pygame.display.update()


def semi_automatic():
    global grid1, grid2, occupied_positions1, occupied_positions2, jugador1, jugador2

    run = True
    clock = pygame.time.Clock()

    while run:
        grid1 = create_grid(jugador1.get_occupied_positions())
        grid2 = create_grid(jugador2.get_occupied_positions())

        x, y = jugador1.atacar()
        result = jugador2.recibir_ataque(x, y)
        jugador1.recibir_resultado(result)

        if result == "L":
            result_to_show.append("Jugador 2 perdió")

        x, y = jugador2.atacar()
        result = jugador1.recibir_ataque(x, y)
        jugador2.recibir_resultado(result)

        if result == "L":
            result_to_show.append("Jugador 1 perdió")

        draw_window(win)
        pygame.display.update()
        pygame.display.set_caption(str(clock.get_fps()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick()

    draw_window(win)
    pygame.display.update()
    pygame.time.delay(1000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(['Presiona A para modo automático', 'o S para semiautomático', "o ESC para salir"], 60, (255, 255, 255), win, 40.0)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_s:
                    semi_automatic()
                if event.key == pygame.K_a:
                    win.fill((0, 0, 0))
                    draw_text_middle(['Simulando....'], 60, (255, 255, 255), win, 0)
                    pygame.display.update()
                    acum_misses_hunt, \
                    acum_hits_hunt, \
                    acum_misses_random, \
                    acum_hits_random, \
                    winner, \
                    winner_points, \
                    loser, \
                    loser_points = noGui.automatic(number_of_simulations)

                    promedio_acum_misses_random = acum_misses_random / number_of_simulations
                    promedio_acum_hits_random = acum_hits_random / number_of_simulations
                    promedio_acum_misses_hunt = acum_misses_hunt / number_of_simulations
                    promedio_acum_hits_hunt = acum_hits_hunt / number_of_simulations

                    porc_hits_hunt = (acum_hits_hunt / (acum_hits_hunt + acum_misses_hunt)) * 100
                    porc_hits_random = (acum_hits_random / (acum_hits_random + acum_misses_random)) * 100

                    result_to_show = []
                    result_to_show.append(
                        "La estrategia ganadora es " + winner + " con " + str(winner_points) + " partidas ganadas.")
                    result_to_show.append(
                        "La estrategia perdedora es " + loser + " con " + str(loser_points) + " partidas ganadas.")
                    result_to_show.append(
                        "Cantidad promedio de tiros acertados con la estrategia hunt and target: " + str(
                            promedio_acum_hits_hunt))
                    result_to_show.append(
                        "Cantidad promedio de tiros errados con la estrategia hunt and target: " + str(
                            promedio_acum_misses_hunt))
                    result_to_show.append("El porcentaje de aciertos fue de: " + str(porc_hits_hunt) + "%")
                    result_to_show.append("Cantidad promedio de tiros acertados con la estrategia random: " + str(
                        promedio_acum_hits_random))
                    result_to_show.append("Cantidad promedio de tiros errados con la estrategia random: " + str(
                        promedio_acum_misses_random))
                    result_to_show.append("El porcentaje de aciertos fue de: " + str(porc_hits_random) + "%")
                    result_to_show.reverse()
                    result_to_show.append("                                  ")
                    result_to_show.append("Presione una tecla para volver al menu")

                    win.fill((0, 0, 0))
                    draw_text_middle(result_to_show, 25,
                                     (255, 255, 255), win, -30)
                    pygame.display.update()

                    finished = False

                    while not finished:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                finished = True

    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Batalla Naval')

main_menu()  # start game
