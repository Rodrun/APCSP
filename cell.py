"""Grid cell object.
"""


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
        
    def showSurrounding(self, gridd): #NOT YET TESTED
        """
        For all of the surrounding cells, change revealed to true.
        Only called when the self.touching == 0.

        Arguments:
        gridd - Parent grid.
        """
        
        for i in range(-1,2):
            for j in range(-1,2):
                a = i + self.i
                b = j + self.j
                if a > -1 and a < self.rows and b > -1 and b < self.cols:
                    neighbor = gridd[a][b]
                    neighbor.revealed = True
        print("All surrounding cells revealed.")
