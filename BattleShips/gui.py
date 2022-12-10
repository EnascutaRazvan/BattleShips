import math

import pygame
import ctypes

# improving the resolution
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# initialize pygame
pygame.init()
pygame.display.set_caption("Battleship")

# global variables
# size of every square
SIZE_SQUARE = 45
# horizontal margin distance
HORIZONTAL_M = SIZE_SQUARE * 4
# vertical margin distance
VERTICAL_M = SIZE_SQUARE

WIDTH = SIZE_SQUARE * 10 * 2 + HORIZONTAL_M
HEIGHT = SIZE_SQUARE * 10 * 2 + VERTICAL_M
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
GREY = (40, 50, 60)
WHITE = (255, 255, 255)


# function to draw a grid

def draw_grid(left=0, top=0):
    for i in range(0, 100):
        x = left + i % 10 * SIZE_SQUARE
        y = top + math.floor(i / 10) * SIZE_SQUARE
        square = pygame.Rect(x, y, SIZE_SQUARE, SIZE_SQUARE)
        pygame.draw.rect(SCREEN, WHITE, square, width=2)


# pygame loop
working = True
pause = False
while working:

    # iterate through events
    for event in pygame.event.get():

        # close the window
        if event.type == pygame.QUIT:
            working = False

        # check the keys that user pressed down
        if event.type == pygame.KEYDOWN:
            # in this case the game will end up
            if event.key == pygame.K_ESCAPE:
                working = False

            # space bar to pause/unpause the game
            if event.key == pygame.K_SPACE:
                print(event.key)
                pause = not pause

    # the execution
    if not pause:
        # draw the background
        SCREEN.fill(GREY)

        #   draw the search grids
        draw_grid()
        draw_grid(left=(WIDTH-HORIZONTAL_M)//2 + HORIZONTAL_M, top=0)

        # draw the position grids
        draw_grid(left=0, top=(HEIGHT-VERTICAL_M)//2 + VERTICAL_M)
        draw_grid(left=(WIDTH-HORIZONTAL_M)//2 + HORIZONTAL_M, top=(HEIGHT-VERTICAL_M)//2 + VERTICAL_M)

        # update the screen
        pygame.display.flip()
