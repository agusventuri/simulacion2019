import pygame
import random
import sys
from models.Boat import Boat
from models.Jugador import Jugador
from models.Strategy import RandomStrategy
from models.Strategy import HuntAndTargetStrategy
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


class Cell(object):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.color = state_colors[STATES.index(state)]


def create_grid(occupied_positions={}):
    grid = [[(0, 0, 131) for x in range(0, 100)] for x in range(0, 100)]

    for key in occupied_positions:
        grid[key[0]][key[1]] = occupied_positions[key]

    #for x in range(0, 100):
    #    for y in range(0, 100):
    #        if (y, x) in occupied_positions:
    #            c = occupied_positions[(y, x)]
    #            grid[x][y] = c
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


def draw_window(surface):
    global grid1, grid2
    surface.fill((0, 0, 0))
    # Tetris Title
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


def main():
    global grid1, grid2, occupied_positions1, occupied_positions2, jugador1, jugador2

    # occupied_positions = {}  # (x,y):(255,0,0)
    boat0 = Boat(True, 6, 90, 50, ["G", "G", "O", "G", "G", "O"])
    boat1 = Boat(False, 6, 80, 10, ["G", "O", "O", "G", "G", "O"])
    boat2 = Boat(True, 5, 70, 20, ["G", "G", "O", "G", "G"])
    boat3 = Boat(False, 5, 60, 30, ["G", "O", "O", "G", "G"])
    boat4 = Boat(True, 4, 50, 40, ["G", "G", "O", "G"])
    boat5 = Boat(False, 4, 40, 50, ["G", "G", "O", "G"])
    boat6 = Boat(True, 3, 30, 60, ["G", "G", "O"])
    boat7 = Boat(False, 3, 20, 70, ["G", "O", "O"])
    boat8 = Boat(True, 2, 10, 80, ["G", "G"])
    boat9 = Boat(False, 2, 50, 90, ["G", "O"])

    #occupied_positions1 = boat0.get_cell(occupied_positions1)
    #occupied_positions1 = boat1.get_cell(occupied_positions1)
    #occupied_positions1 = boat2.get_cell(occupied_positions1)
    #occupied_positions1 = boat3.get_cell(occupied_positions1)
    #occupied_positions1 = boat4.get_cell(occupied_positions1)
    #occupied_positions1 = boat5.get_cell(occupied_positions1)
    #occupied_positions1 = boat6.get_cell(occupied_positions1)
    #occupied_positions1 = boat7.get_cell(occupied_positions1)
    #occupied_positions1 = boat8.get_cell(occupied_positions1)
    #occupied_positions1 = boat9.get_cell(occupied_positions1)

    boat20 = Boat(True, 6, 50, 90, ["G", "G", "O", "G", "G", "O"])
    boat21 = Boat(False, 6, 10, 10, ["G", "O", "O", "G", "G", "O"])
    boat22 = Boat(True, 5, 20, 20, ["G", "G", "O", "G", "G"])
    boat23 = Boat(False, 5, 30, 30, ["G", "O", "O", "G", "G"])
    boat24 = Boat(True, 4, 40, 40, ["G", "G", "O", "G"])
    boat25 = Boat(False, 4, 50, 40, ["G", "G", "O", "G"])
    boat26 = Boat(True, 3, 60, 60, ["G", "G", "O"])
    boat27 = Boat(False, 3, 70, 70, ["G", "O", "O"])
    boat28 = Boat(True, 2, 80, 80, ["G", "G"])
    boat29 = Boat(False, 2, 90, 90, ["G", "O"])

    #occupied_positions2 = boat20.get_cell(occupied_positions2)
    #occupied_positions2 = boat21.get_cell(occupied_positions2)
    #occupied_positions2 = boat22.get_cell(occupied_positions2)
    #occupied_positions2 = boat23.get_cell(occupied_positions2)
    #occupied_positions2 = boat24.get_cell(occupied_positions2)
    #occupied_positions2 = boat25.get_cell(occupied_positions2)
    #occupied_positions2 = boat26.get_cell(occupied_positions2)
    #occupied_positions2 = boat27.get_cell(occupied_positions2)
    #occupied_positions2 = boat28.get_cell(occupied_positions2)
    occupied_positions2 = boat29.get_cell(occupied_positions2)

    run = True
    clock = pygame.time.Clock()

    while run:
        grid1 = create_grid(jugador1.get_occupied_positions())
        grid2 = create_grid(jugador2.get_occupied_positions())

        x, y = jugador1.atacar()
        jugador2.recibir_ataque(x, y)

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
    main()
    #run = True
    #while run:
    #    win.fill((0, 0, 0))
    #    draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
    #    pygame.display.update()
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            run = False

    #        if event.type == pygame.KEYDOWN:
    #            main()
    #pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Batalla naval')

main_menu()  # start game