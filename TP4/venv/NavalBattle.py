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
                             top_left_y + (play_height / 2) - (label.get_height() / 2) + offset))
        offset += y_offset


def draw_window(surface):
    global grid1, grid2
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Batalla naval', 1, (255, 255, 255))

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
            print("Jugador 2 perdió")

        x, y = jugador2.atacar()
        result = jugador1.recibir_ataque(x, y)
        jugador2.recibir_resultado(result)

        if result == "L":
            print("Jugador 1 perdió")

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
        draw_text_middle(['Presiona A para modo automático', 'o S para semiautomático'], 60, (255, 255, 255), win, 30.0)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    semi_automatic()
                if event.key == pygame.K_a:
                    # draw_text_middle(['Simulando....'], 60, (255, 255, 255), win, 0)
                    vector_misses_hunt, \
                        vector_hits_hunt, \
                        vector_misses_random, \
                        vector_hits_random, \
                        winner, \
                        winner_points, \
                        loser, \
                        loser_points = noGui.automatic()

                    cantidad_misses_random = vector_misses_random[0]
                    cantidad_hits_random = vector_hits_random[0]
                    cantidad_misses_hunt = vector_misses_hunt[0]
                    cantidad_hits_hunt = vector_hits_hunt[0]

                    for i in range(1, len(vector_hits_hunt)):
                        cantidad_misses_random = (((i - 1) * cantidad_misses_random) + vector_misses_random[i]) / i
                        cantidad_hits_random = (((i - 1) * cantidad_hits_random) + vector_hits_random[i]) / i
                        cantidad_misses_hunt = (((i - 1) * cantidad_misses_hunt) + vector_misses_hunt[i]) / i
                        cantidad_hits_hunt = (((i - 1) * cantidad_hits_hunt) + vector_hits_hunt[i]) / i

                    porc_hits_hunt = (cantidad_hits_hunt / (cantidad_hits_hunt + cantidad_misses_hunt)) * 100
                    porc_hits_random = (cantidad_hits_random / (cantidad_hits_random + cantidad_misses_random)) * 100

                    print("La estrategia ganadora es " + winner + " con "
                          + str(winner_points) + " partidas ganadas.")
                    print("La estrategia perdedora es " + loser + " con "
                          + str(loser_points) + " partidas ganadas.")
                    print("Cantidad promedio de tiros acertados con la estrategia hunt and target: "
                          + str(cantidad_hits_hunt))
                    print("Cantidad promedio de tiros errados con la estrategia hunt and target: "
                          + str(cantidad_misses_hunt))
                    print("El porcentaje de aciertos fue de: "
                          + str(porc_hits_hunt) + "%")
                    print("Cantidad promedio de tiros acertados con la estrategia random: "
                          + str(cantidad_hits_random))
                    print("Cantidad promedio de tiros errados con la estrategia random: "
                          + str(cantidad_misses_random))
                    print("El porcentaje de aciertos fue de: "
                          + str(porc_hits_random) + "%")

    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Batalla naval')

main_menu()  # start game