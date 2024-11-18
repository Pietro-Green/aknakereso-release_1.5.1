import pygame
pygame.init()   #ez valamiert ide is kell

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)

HEADER_HEIGHT = 100
HORIZONTAL_CELLS = 9
VERTICAL_CELLS = 9
CELL_SIZE = 50
BOMB_COUNT = 10

WINDOW_WIDTH = HORIZONTAL_CELLS * CELL_SIZE
WINDOW_HEIGHT = VERTICAL_CELLS * CELL_SIZE + HEADER_HEIGHT

font = pygame.font.Font('digital-7.ttf', 36)                                    # Betutipus

smiley_image = pygame.image.load('smiley.png')                                  # Allapotjelzo
smiley_O_O_image = pygame.image.load('smiley_O_O.png')
smiley_dead_image = pygame.image.load('smiley_dead.png')
smiley_winner_image = pygame.image.load('smiley_winner.png')

cell_images = {                                                                 # Texturak
    "0": pygame.image.load('Cells/0.png'),
    "1": pygame.image.load('Cells/1.png'),
    "2": pygame.image.load('Cells/2.png'),
    "3": pygame.image.load('Cells/3.png'),
    "4": pygame.image.load('Cells/4.png'),
    "5": pygame.image.load('Cells/5.png'),
    "6": pygame.image.load('Cells/6.png'),
    "7": pygame.image.load('Cells/7.png'),
    "8": pygame.image.load('Cells/8.png'),
    "hidden": pygame.image.load('Cells/hidden.png'),
    "flagged": pygame.image.load('Cells/flagged.png'),
    "incorrectly_flagged": pygame.image.load('Cells/incorrectly_flagged.png'),
    "killer_mine": pygame.image.load('Cells/killer_mine.png'),
    "mine": pygame.image.load('Cells/mine.png'),
    "QM": pygame.image.load('Cells/QM.png'),
}
