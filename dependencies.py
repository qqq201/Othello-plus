import numpy as np
import pygame

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (44, 62, 80)
WHITE = (255, 255, 255)
SHADOW = (189, 195, 199)
GREEN = (26, 188, 156)
DARK_GREEN = (22, 160, 133)
GRAY = (52, 73, 94)
YELLOW = (255, 204, 51)

ROWS, COLS = 8, 8
size = WIDTH, HEIGHT = 720, 480

OFFSET = 50
CELL_SIZE = 40

pygame.init()

fonts = {
    "small": pygame.font.Font("assets/fonts/seguisym.ttf", 20),
    "large": pygame.font.Font("assets/fonts/seguisym.ttf", 40)
}

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Othello plus')
pygame.display.set_icon(pygame.image.load('assets/icons/logo.png'))
