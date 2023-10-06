# Multi-Snake (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys,math
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
CELLSIZE = 20
RADIUS = math.floor(CELLSIZE/2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLUE      = (  0,   0, 255)
DARKBLUE  = (  0,   0, 155)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Multi-Snake')

    print("Cell width", CELLWIDTH)
    print("Cell height", CELLHEIGHT)

    print("window width", WINDOWWIDTH)
    print("window height", WINDOWHEIGHT)

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():

    # Get starting worm coordinates
    wormCoords = setStartWormPos()
    wormCoords2 = setStartWormPos()
    
    direction = RIGHT
    direction2 = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()
    apple2 = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == K_RIGHT and direction != LEFT:
                    direction = RIGHT
                elif event.key == K_UP and direction != DOWN:
                    direction = UP
                elif event.key == K_DOWN and direction != UP:
                    direction = DOWN

                elif event.key == K_a and direction2 != RIGHT:
                    direction2 = LEFT
                elif event.key == K_d and direction2 != LEFT:
                    direction2 = RIGHT
                elif event.key == K_w and direction2 != DOWN:
                    direction2 = UP
                elif event.key == K_s and direction2 != UP:
                    direction2 = DOWN
                
                elif event.key == K_ESCAPE:
                    terminate()


        # Check if worms hit wall or self
        worm = checkWormSelfCollison(wormCoords)
        worm2 = checkWormSelfCollison(wormCoords2)

        wormColor = GREEN
        worm1Color = BLUE

        if (worm):
            wormColor = WHITE

        if (worm2):
            worm1Color = WHITE

        if (worm and worm2):
            # Game over
            return

        a = " "
        # See if worms hit apple
        a = checkAppleCollison(wormCoords, apple, apple2)
        a2 = checkAppleCollison(wormCoords2, apple, apple2)
        
        if a == 'a' or a2 == 'a':
            apple = getRandomLocation()
        elif a == 'a2' or a2 == 'a2':
            apple2 = getRandomLocation()

        # Move worms
        #if (worm == None):
        newHead = moveWorm(direction, wormCoords)
        wormCoords.insert(0, newHead)   #have already removed the last segment
        
        #if (worm2 == None):
        newHead2 = moveWorm(direction2, wormCoords2)
        wormCoords2.insert(0, newHead2)   #have already removed the last segment

        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords, DARKGREEN, wormColor)
        drawWorm(wormCoords2, DARKBLUE, worm1Color)
        drawApple(apple)
        drawApple(apple2)
        drawScore(len(wormCoords) - 3, 1, GREEN)
        drawScore(len(wormCoords2) - 3, 0, BLUE)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def setStartWormPos():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)

    return [{'x': startx,     'y': starty},
            {'x': startx - 1, 'y': starty},
            {'x': startx - 2, 'y': starty}]  


def checkWormSelfCollison(wormCoords):
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return True# game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return True # game over


def checkAppleCollison(wormCoords, apple, apple2):
        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            #apple = getRandomLocation() # set a new apple somewhere
            return "a"
        
        elif wormCoords[HEAD]['x'] == apple2['x'] and wormCoords[HEAD]['y'] == apple2['y']:
            # don't remove worm's tail segment
            #apple2 = getRandomLocation() # set a new apple somewhere
            return "a2"
            
        else:
            del wormCoords[-1] # remove worm's tail segment
            return "aNot"


def moveWorm(direction, wormCoords):
        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            return {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            return {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            return {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            return {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Multi-Snake', True, WHITE, BLUE)
    titleSurf2 = titleFont.render('Agents', True, YELLOW)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


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
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
    overRect.midtop = (math.floor(WINDOWWIDTH / 2), gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score, position, scoreColor):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, scoreColor)
    scoreRect = scoreSurf.get_rect()
    
    if position == 0:
        scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    else:
        scoreRect.topright = (120, 10)

    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, outerColor, innerColor):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, outerColor, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, innerColor, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    xcenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE/2)
    ycenter = coord['y'] * CELLSIZE+ math.floor(CELLSIZE/2)
    #appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    #pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    pygame.draw.circle(DISPLAYSURF, RED,(xcenter,ycenter),RADIUS)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()