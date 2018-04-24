import os, sys
import pygame
from pygame.locals import *
from random import *

pygame.font.init()

if not pygame.font: 
    print('Warning, fonts disabled')
else:
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
if not pygame.mixer: print('Warning, sound disabled')



pygame.init()

gameDisplay = pygame.display.set_mode((800,600))

pygame.display.set_caption("Minesweeper")

rows = 9
cols = 9
w = 50
gray = (127,127,127)
bombImg = pygame.image.load('bomb.jpg')
bombImg = pygame.transform.scale(bombImg, (w,w))

endGame = False

class Cell(object):

    def __init__(self,x,y,w):
        self.x = x*w
        self.y = y*w
        self.w = w
        self.bomb = False
        self.revealed = True
        self.color = (127,127,127)
        self.cellID = ""
        self.touching = 0

    def getTouching(self,x,y,gridd):
        if self.bomb == True:
            return -1
        total = 0
        for i in range(-1,1):
            for j in range(-1,1):
                a = i + x
                b = j + y
                if a > -1 and a < rows and b > -1 and b < cols:
                    neighbor = gridd[a][b]
                    if neighbor.bomb == True:
                        total = total + 1
        self.touching = total


def make2DArray(rows,cols):
    mainArray = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(len(mainArray)):
        for j in range(len(mainArray[i])):
            mainArray[i][j] = Cell(i,j,w)
            ri = randint(0,4)
            #print(ri)
            if ri == 1:
                mainArray[i][j].bomb = True
    return mainArray
#def funct():     i = 0
    # j = 0
    # mainArray = []
    # arr = []
    # for i in range(rows):

    #     for j in range(cols):
    #         x = Cell(i,j,w)
    #         x.cellID = (i,j)
    #         arr.insert(j, x)
    #         ri = randint(0,4)
    #         #print(ri)
    #         if ri == 1:
    #             x.bomb = True

    #     mainArray.insert(i, arr)

    # return mainArray

def drawGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(gameDisplay, grid[i][j].color, [grid[i][j].x, grid[i][j].y, grid[i][j].w-1, grid[i][j].w-1])
            if grid[i][j].revealed == True: 
                if grid[i][j].bomb == True:
                    gameDisplay.blit(bombImg, (grid[i][j].x, grid[i][j].y))
                if grid[i][j].bomb == False:
                    gameDisplay.blit(myfont.render(str(grid[i][j].touching), True, (255,0,0)), (grid[i][j].x+15, grid[i][j].y))
                    pass

grid = make2DArray(rows,cols)

for i in range(len(grid)):
    for j in range(len(grid[i])):
        grid[i][j].getTouching(j,i,grid)

drawGrid(grid)

while not endGame:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            endGame = True

        if event.type == pygame.MOUSEBUTTONUP:
            bomb = False
            #print(event.pos)
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if event.pos[0] > grid[i][j].x and event.pos[0] < grid[i][j].x + w and event.pos[1] > grid[i][j].y and event.pos[1] < grid[i][j].y + w:
                            grid[i][j].color = (90,90,90)
                            grid[i][j].revealed = True
                            drawGrid(grid)
                            if grid[i][j].bomb == True:
                                bomb = True
                            else:
                                print("Touching: ",grid[i][j].touching)
            print("Bomb clicked: ",bomb)
            
    pygame.display.update()

pygame.quit()
quit()