# Main file for Atanki, the Atari tank game knockoff.
# Assembled using base code from wormy.py.

# Worked on by Adam Campbell, Rory Kerr and Connor Barthelmie.

import random, pygame, sys,
from pygame.locals import *

# -----------------------------------------------------------------------------------------------------------------------------------------
# GRAPHICS SETUP

FPS = 20
WINDOWWIDTH = 1600
WINDOWHEIGHT = 900
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = GREEN

# ----------------------------------------------------------------------------------------------------------------------------------------

# RANDOM START CODE FOR ENEMIES
# gStartx = random.randint(5, CELLWIDTH - 6)
# gStarty = random.randint(5, CELLHEIGHT - 6)
# gWormCoords = [{'x': gStartx,     'y': gStarty},
#               {'x': gStartx - 1, 'y': gStarty},
#               {'x': gStartx - 2, 'y': gStarty}]
# gDirection = RIGHT

# -----------------------------------------------------------------------------------------------------------------------------------------
# GAME CODE AND FUNCTIONS

# Set directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    init()
    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def init():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')
    
def game_init():
    global gTankCoords, gDirection

    # Set a random start point.
    gStartx = random.randint(5, CELLWIDTH - 6)
    gStarty = random.randint(5, CELLHEIGHT - 6)
    gTankCoords = [{'x': gStartx,     'y': gStarty},
    gDirection = UP
    
def runGame():
    game_init()    
    while True: # main game loop
        game_over = game_update()
        game_render()
        if game_over == True:
            return # game over, stop running the game
# ------------------------------------------------------------------------------------------------------------------------------------------
# ALMOST ALL NEW CODE WILL PROBABLY GO IN GAME_UPDATE. ANYTHING RELEVANT TO NON-SETUP HERE.                   
                   
def game_update():
    global gWormCoords, gDirection, gApple

    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and gDirection != RIGHT:
                gDirection = LEFT
            elif (event.key == K_RIGHT or event.key == K_d) and gDirection != LEFT:
                gDirection = RIGHT
            elif (event.key == K_UP or event.key == K_w) and gDirection != DOWN:
                gDirection = UP
            elif (event.key == K_DOWN or event.key == K_s) and gDirection != UP:
                gDirection = DOWN
            elif event.key == K_ESCAPE:
                terminate()
                   
# ------------------------------------------------------------------------------------------------------------------------------------------
                   
def game_render():
    DISPLAYSURF.fill(BGCOLOR)
    drawGrid()
    drawWorm(gWormCoords)
    drawApple(gApple)
    drawScore(len(gWormCoords) - 3)
    pygame.display.update()
    FPSCLOCK.tick(FPS)
                   
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
                   
# KRT 14/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:      #event is quit 
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   #event is escape key
                terminate()
            else:
                return event.key   #key found return with it
    # no quit or key events in queue so return None    
    return None
                   

def terminate():
    pygame.quit()
    sys.exit()
                   
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
                   
def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue 
    while True:
        if checkForKeyPress():
            return
#KRT 12/06/2012 reduce processor loading in gameover screen.
        pygame.time.wait(100)
                   
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
