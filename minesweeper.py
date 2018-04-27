"""
Minesweeper game.
"""
import os
import sys
from random import randint

import pygame
from pygame.locals import *  # Preferably don't wildcard import

from cell import Cell


pygame.font.init()

if not pygame.font:
    print("Warning, fonts disabled")
else:
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
if not pygame.mixer:
    print("Warning, sound disabled")


pygame.init()

gameDisplay = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Minesweeper")

rows = 9
cols = 9
w = 50
GRAY = (127, 127, 127)  # Unused?
bombImg = pygame.image.load("bomb.jpg")
bombImg = pygame.transform.scale(bombImg, (w, w))

endGame = False


def make2DArray(rows, cols) -> list:
    """
    Generate a 2D list of safe and bomb cells.

    Arguments:
    rows - Number of rows.
    cols - Number of columns.

    Returns:
    List of randomized cells.
    """
    mainArray = [[None for i in range(cols)] for j in range(rows)]

    for i in range(len(mainArray)):
        for j in range(len(mainArray[i])):
            mainArray[i][j] = Cell(i, j, w)
            ri = randint(0, 4)
            # print(ri)
            if ri == 1:
                mainArray[i][j].bomb = True
    return mainArray
# def funct():
#     i = 0
#     j = 0
#     mainArray = []
#     arr = []
#     for i in range(rows):
#         for j in range(cols):
#             x = Cell(i,j,w)
#             x.cellID = (i,j)
#             arr.insert(j, x)
#             ri = randint(0,4)
#             #print(ri)
#             if ri == 1:
#                 x.bomb = True
#         mainArray.insert(i, arr)
#     return mainArray


def drawGrid(grid) -> None:
    """
    Draw the minesweeper grid.

    Arguments:
    grid - 2D list of cells.

    Returns:
    None.
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell = grid[i][j]
            pygame.draw.rect(gameDisplay, cell.color, [
                             cell.x, cell.y, cell.w-1, cell.w-1])
            if cell.revealed == True:
                if cell.bomb == True:
                    gameDisplay.blit(bombImg, (cell.x, cell.y))
                if cell.bomb == False:
                    if(cell.touching > 0):
                        gameDisplay.blit(myfont.render(str(cell.touching),
                                                       True,
                                                       (255, 0, 0)),
                                         (cell.x+15, cell.y))


# Generate grid
grid = make2DArray(rows, cols)
# Count adjacent bombs
for i in range(len(grid)):
    for j in range(len(grid[i])):
        grid[i][j].getTouching(grid)

drawGrid(grid)

while not endGame:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            endGame = True

        if event.type == pygame.MOUSEBUTTONUP:
            bomb = False
            # print(event.pos)
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    cell = grid[i][j]
                    if event.pos[0] > cell.x \
                        and event.pos[0] < cell.x + w \
                        and event.pos[1] > cell.y \
                        and event.pos[1] < cell.y + w:
                        cell.color = (90, 90, 90)
                        cell.revealed = True
                        drawGrid(grid)
                        if cell.bomb == True:
                            bomb = True
                        else:
                            print("Touching: ", cell.touching)
                            if cell.touching == 0: #NOT TESTED
                                cell.showSurrounding(grid) #NOT TESTED
            print("Bomb clicked: ", bomb)

    pygame.display.update()

pygame.quit()
