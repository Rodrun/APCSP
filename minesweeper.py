"""
Minesweeper game.
"""
import os
import sys
from random import randint

import pygame
from pygame.locals import *  # Preferably don't wildcard import

from cell import Cell
from grid import Grid


pygame.init()

rows = 9
cols = 9
w = 50
bombImg = pygame.image.load("bomb.jpg")
bombImg = pygame.transform.scale(bombImg, (w, w))

endGame = False

class Minesweeper(object):
    def __init__(self,rows,cols,w):
        self.rows = rows
        self.cols = cols
        self.w = w
        self.grid = Grid(rows,cols)

        for i in range(len(self.grid.array)):
            for j in range(len(self.grid.array[i])):
                self.grid.array[i][j].getTouching(self.grid.array)
        
    
    def drawGrid(self):
        self.grid.drawGrid()

minesweeper = Minesweeper(rows,cols,w)

minesweeper.drawGrid()

while not endGame:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            endGame = True

        if event.type == pygame.MOUSEBUTTONUP:
            bomb = False
            # print(event.pos)
            for i in range(len(minesweeper.grid.array)):
                for j in range(len(minesweeper.grid.array[i])):
                    cell = minesweeper.grid.array[i][j]
                    if event.pos[0] > cell.x \
                        and event.pos[0] < cell.x + w \
                        and event.pos[1] > cell.y \
                        and event.pos[1] < cell.y + w:
                        cell.action()

    pygame.display.update()

pygame.quit()
