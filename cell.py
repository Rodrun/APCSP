"""Grid cell object.
"""

import pygame
from pygame.locals import *

bombImg = pygame.image.load("bomb.jpg")
bombImg = pygame.transform.scale(bombImg, (50, 50)) #Change 50s to scale later

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Minesweeper")

pygame.font.init()

if not pygame.font:
    print("Warning, fonts disabled")
else:
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
if not pygame.mixer:
    print("Warning, sound disabled")

# TODO: derive from pygame.sprite.Sprite
class Cell:

    def __init__(self, x, y, w, rows=9, cols=9):
        """
        Arguments:
        x - X coordinate.
        y - Y coordinate.
        w - Width of cell.
        rows - Rows of parent grid.
        cols - Columns of parent grid.
        """
        self.i = x
        self.j = y
        self.x = x*w
        self.y = y*w
        self.w = w
        self.bomb = False
        self.revealed = False
        self.color = (127,127,127)
        self.touching = 0
        self.rows = rows
        self.cols = cols
        self.actDebounce = False

    def getTouching(self, gridd):
        """
        Get the total amount of touching bomb cells and assign to object
        member 'touching'.
        Arguments:
        gridd - Parent grid.
        Returns:
        -1 if bomb, otherwise None.
        """
        if self.bomb == True:
            return -1
        total = 0
        for i in range(-1,2):
            for j in range(-1,2):
                a = i + self.i
                b = j + self.j
                if a > -1 and a < self.rows and b > -1 and b < self.cols:
                    neighbor = gridd[a][b]
                    if neighbor.bomb == True:
                        total = total + 1
        self.touching = total

    def action(self):
        """
        Draw over the current image for the cell with the new information.
        """
        if self.actDebounce == False:
            self.color = (90, 90, 90)
            self.revealed = True

            if self.bomb == True:
                gameDisplay.blit(bombImg, (self.x, self.y))
            else:
                pygame.draw.rect(gameDisplay, self.color, [
                                self.x, self.y, self.w-1, self.w-1])
                if self.touching > 0:
                    gameDisplay.blit(myfont.render(str(self.touching),
                                    True,
                                    (255, 0, 0)),
                                    (self.x+15, self.y))
                if self.touching == 0:
                    self.showSurrounding()

            self.actDebounce = True

    def showSurrounding(self): #NOT YET TESTED
        """
        For all of the surrounding cells, reveal.
        Only called when the self.touching == 0.
        """
        
        for i in range(-1,2):
            for j in range(-1,2):
                a = i + self.i
                b = j + self.j
                if a > -1 and a < self.rows and b > -1 and b < self.cols:
                    #DEFINE NEIGHBOR SOMEHOW
                    neighbor.action()
        print("All surrounding cells revealed.")
