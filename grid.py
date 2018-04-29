"""
Grid Object
"""

import pygame
from pygame.locals import *  # Preferably don't wildcard import

from cell import Cell
from random import randint

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Minesweeper")


class Grid(object):

    def __init__(self,rows,cols):
        """
        Generate a 2D list of safe and bomb cells.
        Arguments:
        rows - Number of rows.
        cols - Number of columns.
        w = 50
        """
        self.array = [[None for i in range(cols)] for j in range(rows)]
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                w = 50
                self.array[i][j] = Cell(i, j, w)
                ri = randint(0, 4)
                # print(ri)
                if ri == 1:
                    self.array[i][j].bomb = True
        for i in range(len(self.array)):
            for j in range(len(self.array[j])):
                self.getNeighbors(self.array[i][j], self.array, rows, cols)
        
        
                
    def drawGrid(self):
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                cell = self.array[i][j]
                pygame.draw.rect(gameDisplay, cell.color, [
                                cell.x, cell.y, cell.w-1, cell.w-1])
                # if cell.revealed == True:
                #     if cell.bomb == True:
                #         gameDisplay.blit(bombImg, (cell.x, cell.y))
                #     if cell.bomb == False:
                #         if(cell.touching > 0):
                #             gameDisplay.blit(myfont.render(str(cell.touching),
                #                             True,
                #                             (255, 0, 0)),
                #                             (cell.x+15, cell.y))
    
    def getNeighbors(self,cell,grid,rows,cols):
            for a in range(-1,2):
                for b in range(-1,2):
                    c = cell.i + a
                    d = cell.j + b
                    if c > -1 and c < rows and d > -1 and d < cols:
                        neighbor = grid[c][d]
                        grid[cell.i][cell.j].surrounding.insert(0, neighbor)
