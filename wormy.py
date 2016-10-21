# Main file for Atanki, the Atari tank game knockoff.
# Assembled using base code from wormy.py.

# Worked on by Adam Campbell, Rory Kerr and Connor Barthelmie.

import random, pygame, sys
from pygame.locals import *

# -----------------------------------------------------------------------------------------------------------------------------------------
# GRAPHICS SETUP

FPS = 20
WINDOWWIDTH = 900
WINDOWHEIGHT = 460
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
width = 45
height =  45
Matrix = [[0 for x in range(width)] for y in range(height)] 

##DRAWING THE MAP
for height in range (0,45):
    for width in range (0,45):
        if width ==0:
            Matrix[width][height] = 1
        elif width ==44:
            Matrix[width][height] = 1
        elif height ==0:
            Matrix[width][height] = 1
        elif height ==22:
            Matrix[width][height] = 1
        else:
            Matrix[width][height] = 0
            
            
            

for i in range (4,10):
    Matrix[4][i]  = 1
    Matrix[4][(i+9)] = 1
    
    Matrix[40][i] = 1
    Matrix[40][i+9] = 1
    
    
for x in range (5,13):
        
    Matrix[x][4] = 1
    Matrix[x][18] = 1
    
    Matrix[x+27][4] = 1
    Matrix[x+27][18] = 1
    
for x in range (8,13):

    Matrix[x+12][7]=1
    Matrix[x+12][15]=1
    
    for y in range(8,15):
        Matrix[x][y]=1
        Matrix[x+24][y]=1


for i in range (4,8):
    Matrix[16][i]  = 1
    Matrix[16][(i+11)] = 1
    
    Matrix[28][i] = 1
    Matrix[28][i+11] = 1
    
for y in range(1,8):
    Matrix[20][y] = 1
    Matrix[24][y] = 1
    
    Matrix[20][y+14] = 1
    Matrix[24][y+14] = 1
    
for x in range(16,29):
    Matrix[x][11] = 1
   
    

gPlayer_X = 2
gPlayer_Y = 2
Matrix[gPlayer_X][gPlayer_Y] = 2

# ----------------------------------------------------------------------------------------------------------------------------------------

# RANDOM START CODE FOR ENEMIES
# gStartx = random.randint(5, CELLWIDTH - 6)
# gStarty = random.randint(5, CELLHEIGHT - 6)
# gWormCoords = [{'x': gStartx,     'y': gStarty},
#               {'x': gStartx - 1, 'y': gStarty},
#               {'x': gStartx - 2, 'y': gStarty}]
# 

# -----------------------------------------------------------------------------------------------------------------------------------------
# GAME CODE AND FUNCTIONS

# Set directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
gDirection = UP
turretDir = UP

# Load art assets (from same directory as python)
sTank = pygame.image.load('GoodTank.png')
sGoodGun = pygame.image.load('TankGunGood.png')
sBullet = pygame.image.load('Bullet.png')
sFloor = pygame.image.load('TileFloor.png')
sWall = pygame.image.load('TileWall.png')

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

    global gPlayer_X, gPlayer_Y, gDirection

    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a):
                if Matrix[(gPlayer_X-1)][gPlayer_Y]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_X -= 1
                    gDirection = LEFT
                    turretDir = LEFT
            elif (event.key == K_RIGHT or event.key == K_d):
                if Matrix[(gPlayer_X+1)][gPlayer_Y]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_X += 1
                    gDirection = RIGHT
                    turretDir = RIGHT
            elif (event.key == K_UP or event.key == K_w):
                if Matrix[(gPlayer_X)][gPlayer_Y-1]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_Y -= 1
                    gDirection = UP
                    turretDir = UP
            elif (event.key == K_DOWN or event.key == K_s):
                if Matrix[(gPlayer_X)][gPlayer_Y+1]!=1:
                    Matrix[gPlayer_X][gPlayer_Y] = 0
                    gPlayer_Y += 1
                    gDirection = DOWN
                    turretDir = DOWN
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
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))

def drawMap():
    global sTank, sGoodGun, sFloor, sWall, gDirection, turretDir
    
    
    for y in range(0, 45):
        for x in range (0, 45):
            if Matrix[x][y] == 0:
                DISPLAYSURF.blit(sFloor, (x*CELLSIZE,y*CELLSIZE))
            elif Matrix[x][y] == 1:
                DISPLAYSURF.blit(sWall, (x*CELLSIZE,y*CELLSIZE))
            elif Matrix[x][y] == 2:
                #Draw Tank
                # Scales the image
                sImage = pygame.transform.scale(sTank, (CELLSIZE, CELLSIZE))
                # Rotates the image
                if gDirection == LEFT:
                    sImageRotated = pygame.transform.rotate(sImage, 90)
                elif gDirection == DOWN:
                    sImageRotated = pygame.transform.rotate(sImage, 180)
                elif gDirection == RIGHT:
                    sImageRotated = pygame.transform.rotate(sImage, 270)
                else:
                    sImageRotated = sImage
                DISPLAYSURF.blit(sImageRotated, (x*CELLSIZE,y*CELLSIZE))
                #Draw Turret
                # Scales the image
                sImage = pygame.transform.scale(sGoodGun, (CELLSIZE, CELLSIZE))
                # Rotates the image
                if turretDir == LEFT:
                    sImageRotated = pygame.transform.rotate(sImage, 90)
                elif turretDir == DOWN:
                    sImageRotated = pygame.transform.rotate(sImage, 180)
                elif turretDir == RIGHT:
                    sImageRotated = pygame.transform.rotate(sImage, 270)
                else:
                    sImageRotated = sImage
                DISPLAYSURF.blit(sImageRotated, (x*CELLSIZE,y*CELLSIZE))
                
            

if __name__ == '__main__':
    main()
