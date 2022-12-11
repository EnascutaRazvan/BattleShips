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
SIZE_SQUARE = 40
# horizontal margin distance
HORIZONTAL_M = SIZE_SQUARE * 4
# vertical margin distance
INDENT = SIZE_SQUARE
# the way that the ships looks into the grid
BEAUTIFIER_INDENT = 7

# indentation left right up down


WIDTH = SIZE_SQUARE * 10 + INDENT * 2
HEIGHT = SIZE_SQUARE * 10 * 2 + INDENT + INDENT * 2
PHASE = 0
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
while working:

    # iterate through events
    for event in pygame.event.get():

        # close the window
        if event.type == pygame.QUIT:
            working = False
        # user mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and not pause and PHASE != -1:
            x, y = pygame.mouse.get_pos()
            print(x, y)
            if game.player_turn1 and x > INDENT and x < SIZE_SQUARE * 10 + INDENT \
                    and y > INDENT and y < SIZE_SQUARE * 10 + INDENT:
                print("asd")
                row = (y - INDENT) // SIZE_SQUARE
                col = (x - INDENT) // SIZE_SQUARE
                i = row * 10 + col
                if game.player1.search[i] == "U":
                    game.make_move(i)
                    if game.winner != "":
                        print(f"The winner is {game.winner}")
                        PHASE = -1

            if game.player_turn2 and x > INDENT and x < SIZE_SQUARE * 10 + INDENT \
                    and y > (HEIGHT - 2 * INDENT) - SIZE_SQUARE * 10 and y < HEIGHT - INDENT:
                print("asdasda")
                row = (y - INDENT * 2 - SIZE_SQUARE * 10) // SIZE_SQUARE
                print(row)
                col = (x - INDENT) // SIZE_SQUARE
                print(col)
                i = row * 10 + col
                print(i)
                if game.player2.search[i] == "U":
                    game.make_move(i)
                    if game.winner != "":
                        print(f"The winner is {game.winner}")
                        PHASE = -1

        # check the keys that user pressed down
        if event.type == pygame.KEYDOWN:
            print(event.key)
            # in this case the game will end up
            if event.key == pygame.K_ESCAPE:
                working = False

            # space bar to pause/unpause the game
            if event.key == pygame.K_SPACE:
                print(event.key)
                pause = not pause

            # enter to advance in the new phase
            if event.key == 13 and PHASE != -1:
                PHASE += 1

    # the execution
    if not pause:
        # draw the background
        SCREEN.fill(GREY)

        # First phase draw the positions grid along with the ships of player 1
        if PHASE == 0:
            draw_grid(player=game.player1, left=INDENT, top=INDENT)
            draw_ships(player=game.player1, left=INDENT, top=INDENT)
            font = pygame.font.Font('freesansbold.ttf', 32)
            text1 = font.render('Player 1', True, RED, GREY)
            textRect1 = text1.get_rect()
            textRect1.center = (WIDTH // 2, (INDENT // 2))
            SCREEN.blit(text1, textRect1)
        # Second phase draw the positions grid along with the ships of player 2
        if PHASE == 1:
            SCREEN.fill(GREY)
            draw_grid(player=game.player2, top=(HEIGHT + INDENT) // 2, left=INDENT)
            draw_ships(player=game.player2, top=(HEIGHT + INDENT) // 2, left=INDENT)
            font = pygame.font.Font('freesansbold.ttf', 32)
            text2 = font.render('Player 2', True, RED, GREY)
            textRect2 = text2.get_rect()
            textRect2.center = (WIDTH // 2, (HEIGHT // 2))
            SCREEN.blit(text2, textRect2)


        # search grids of both players and start the game
        if PHASE >= 2:
            draw_grid(player=game.player1, left=INDENT, top=INDENT, search=True)
            draw_grid(player=game.player2, top=(HEIGHT + INDENT) // 2, left=INDENT, search=True)
            font = pygame.font.Font('freesansbold.ttf', 32)
            text1 = font.render('Player 1', True, RED, GREY)
            text2 = font.render('Player 2', True, RED, GREY)
            textRect1 = text1.get_rect()
            textRect2 = text2.get_rect()
            textRect1.center = (WIDTH//2,(INDENT // 2))
            textRect2.center = (WIDTH//2, (HEIGHT//2))
            SCREEN.blit(text1,textRect1)
            SCREEN.blit(text2,textRect2)

        if PHASE == -1:
            SCREEN.fill(GREY)
            font = pygame.font.Font('freesansbold.ttf', 32)
            text1 = font.render(f'{game.winner} wins', True, RED, GREY)
            textRect1 = text1.get_rect()
            textRect1.center = (WIDTH//2, HEIGHT//2)
            SCREEN.blit(text1, textRect1)

        # update the screen
        pygame.display.flip()
