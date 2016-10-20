# Main file for Atanki, the Atari tank game knockoff.
# Assembled using base code from wormy.py.

# Worked on by Adam Campbell, Rory Kerr and Connor Barthelmie.

import random, pygame, sys
from pygame.locals import *

# -----------------------------------------------------------------------------------------------------------------------------------------
# GRAPHICS SETUP

FPS = 20
WINDOWWIDTH = 640
WINDOWHEIGHT = 320
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
################################################
##CREATING ARRAY SYSTEM (ANNOYING AS SHIT)
width = 32
height =  32
Matrix = [[0 for x in range(width)] for y in range(height)] 

##DRAWING THE MAP
for height in range (0,32):
    for width in range (0,32):
        if width ==0:
            Matrix[width][height] = 1
        elif width ==31:
            Matrix[width][height] = 1
        elif height ==0:
            Matrix[width][height] = 1
        elif height ==15:
            Matrix[width][height] = 1
        else:
            Matrix[width][height] = 0
            
            
            

for y in range (4,6):
    Matrix[5][y]  = 1
    Matrix[5][(y+6)] = 1
    
    Matrix[10][y]  = 1
    Matrix[10][(y+6)] = 1
    
    Matrix[21][y]  = 1
    Matrix[21][(y+6)] = 1
    
    Matrix[26][y]  = 1
    Matrix[26][(y+6)] = 1

for y in range (6,10):
        
    Matrix[15][y] = 1
    Matrix[16][y] = 1

for y in range (13,16):
    Matrix[15][y] = 1
    Matrix[16][y] = 1

for y in range (0,3):
    Matrix[15][y] = 1
    Matrix[16][y] = 1

gPlayer_X = 3
gPlayer_Y = 3
Matrix[gPlayer_X][gPlayer_Y] = 2

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
    drawMap()
    drawGrid()
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
    gTankCoords = [{'x': gStartx,     'y': gStarty}],
    gDirection = UP
    
def runGame():
    
    game_init()    
    while True: # main game loop
        Matrix[gPlayer_X][gPlayer_Y] = 2
        game_over = game_update()
        game_render()
        if game_over == True:
            return # game over, stop running the game
# ------------------------------------------------------------------------------------------------------------------------------------------
# ALMOST ALL NEW CODE WILL PROBABLY GO IN GAME_UPDATE. ANYTHING RELEVANT TO NON-SETUP HERE.                   
                   
def drawGrid():

    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
        
    
def game_update():

    global gPlayer_X, gPlayer_Y

    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a):
                if Matrix[(gPlayer_X-1)][gPlayer_Y]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_X -= 1
            elif (event.key == K_RIGHT or event.key == K_d):
                if Matrix[(gPlayer_X+1)][gPlayer_Y]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_X += 1
            elif (event.key == K_UP or event.key == K_w):
                if Matrix[(gPlayer_X)][gPlayer_Y-1]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_Y -= 1
            elif (event.key == K_DOWN or event.key == K_s):
                if Matrix[(gPlayer_X)][gPlayer_Y+1]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_Y += 1
            elif event.key == K_ESCAPE:
                terminate()
                
                   
# ------------------------------------------------------------------------------------------------------------------------------------------
                   
def game_render():
    drawMap()
    drawGrid()
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

def drawMap():

    for y in range(0, 32):
        for x in range (0, 32):
            if Matrix[x][y] == 0:
                WallRect = pygame.Rect(x*CELLSIZE, y*CELLSIZE, CELLSIZE, CELLSIZE)
                pygame.draw.rect(DISPLAYSURF, DARKGRAY, WallRect)
            elif Matrix[x][y] == 1:
                FloorRect = pygame.Rect(x*CELLSIZE, y*CELLSIZE, CELLSIZE, CELLSIZE)
                pygame.draw.rect(DISPLAYSURF, RED, FloorRect)
            elif Matrix[x][y] == 2:
                PlayerRect = pygame.Rect(x*CELLSIZE, y*CELLSIZE, CELLSIZE, CELLSIZE)
                pygame.draw.rect(DISPLAYSURF, GREEN, PlayerRect)
            

if __name__ == '__main__':
    main()
