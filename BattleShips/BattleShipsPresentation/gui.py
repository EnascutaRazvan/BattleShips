import math
from engine import *
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
# the way that the ships looks into the grid
BEAUTIFIER_INDENT = 7

WIDTH = SIZE_SQUARE * 10 * 2 + HORIZONTAL_M
HEIGHT = SIZE_SQUARE * 10 * 2 + VERTICAL_M
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
GREY = (40, 50, 60)
WHITE = (255, 255, 255)
GREEN = (50, 200, 150)
RED = (250, 50, 100)
BLUE = (50, 150, 200)
ORANGE = (250, 140, 20)

COLORS_FOR_SEARCH = {"U": GREY, "M": BLUE, "H": ORANGE, "S": RED}


# function to draw a grid

def draw_grid(player, left=0, top=0, search=False):
    for i in range(0, 100):
        x = left + i % 10 * SIZE_SQUARE
        y = top + math.floor(i / 10) * SIZE_SQUARE
        square = pygame.Rect(x, y, SIZE_SQUARE, SIZE_SQUARE)
        pygame.draw.rect(SCREEN, WHITE, square, width=2)
        if search:
            x += SIZE_SQUARE // 2
            y += SIZE_SQUARE // 2
            pygame.draw.circle(SCREEN, COLORS_FOR_SEARCH[player.search[i]], (x, y), radius=SIZE_SQUARE // 4)


# function to draw the ships onto the grid
def draw_ships(player, left=0, top=0):
    for ship in player.ships:
        x = left + ship.col * SIZE_SQUARE + BEAUTIFIER_INDENT
        y = top + ship.row * SIZE_SQUARE + BEAUTIFIER_INDENT

        if ship.orientation == "h":
            width = ship.size * SIZE_SQUARE - 2 * BEAUTIFIER_INDENT
            height = SIZE_SQUARE - 2 * BEAUTIFIER_INDENT
        else:
            width = SIZE_SQUARE - 2 * BEAUTIFIER_INDENT
            height = ship.size * SIZE_SQUARE - 2 * BEAUTIFIER_INDENT
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, GREEN, rect, border_radius=15)


game = Game()

# pygame loop
working = True
pause = False
winner = False
while working:

    # iterate through events
    for event in pygame.event.get():

        # close the window
        if event.type == pygame.QUIT:
            working = False
        # user mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and not pause:
            x, y = pygame.mouse.get_pos()
            if game.player_turn1 and x < SIZE_SQUARE * 10 and y < SIZE_SQUARE * 10:
                row = y // SIZE_SQUARE
                col = x // SIZE_SQUARE

                i = row * 10 + col
                if game.player1.search[i] == "U":
                    game.make_move(i)
                    if game.winner != "":
                        print(f"The winner is {game.winner}")
                        winner = True

            if game.player_turn2 and x > WIDTH - SIZE_SQUARE * 10 and y > SIZE_SQUARE * 10 + VERTICAL_M:
                row = (y - SIZE_SQUARE*10 - VERTICAL_M) // SIZE_SQUARE
                col = (x - SIZE_SQUARE * 10 - HORIZONTAL_M) // SIZE_SQUARE
                i = row * 10 + col
                if game.player2.search[i] == "U":
                    game.make_move(i)
                    if game.winner != "":
                        print(f"The winner is {game.winner}")
                        winner = True
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
        draw_grid(player=game.player1, search=True)
        draw_grid(player=game.player2, left=(WIDTH - HORIZONTAL_M) // 2 + HORIZONTAL_M,
                  top=(HEIGHT - VERTICAL_M) // 2 + VERTICAL_M, search= True)

        # draw the position grids
        draw_grid(player=game.player1, left=0, top=(HEIGHT - VERTICAL_M) // 2 + VERTICAL_M)
        draw_grid(player=game.player2, left=(WIDTH - HORIZONTAL_M) // 2 + HORIZONTAL_M)

        # draw the ships
        draw_ships(game.player1, left=0, top=(HEIGHT - VERTICAL_M) // 2 + VERTICAL_M)
        draw_ships(game.player2, left=(WIDTH - HORIZONTAL_M) // 2 + HORIZONTAL_M, top = 0)

        font = pygame.font.Font('freesansbold.ttf', 32)
        text1 = font.render('Player 1', True, RED, GREY)
        text2 = font.render('Player 2', True, RED, GREY)
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = ((WIDTH-SIZE_SQUARE*10-HORIZONTAL_M)//2, HEIGHT//2)
        textRect2.center = ((SIZE_SQUARE*10 + HORIZONTAL_M + (SIZE_SQUARE*10)//2) , (HEIGHT // 2))
        SCREEN.blit(text1, textRect1)
        SCREEN.blit(text2, textRect2)

        # update the screen
        pygame.display.flip()
        if winner:
            pause = True

    if winner:
        SCREEN.fill(GREY)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text1 = font.render(f'{game.winner} wins', True, RED, GREY)
        textRect1 = text1.get_rect()
        textRect1.center = (WIDTH // 2, HEIGHT // 2)
        SCREEN.blit(text1, textRect1)

        pygame.display.flip()

