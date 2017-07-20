"""
class
"""

from gameoflife import pool
from ui import controlbar, labelbutton

class DisplayedObject(object):
    """description of class"""


    def __init__(self, obj, pos: tuple, size: tuple):
        self.obj = obj
        self.pos = pos
        self.size = size


    def get_range_x(self):
        return range(self.pos[0], self.pos[0] + self.size[0])


    def get_range_y(self):
        return range(self.pos[1], self.pos[1] + self.size[1])
        

    def get_reach(self):
        return (self.pos[0] + self.size[0], self.pos[1] + self.size[1])

    def is_in_range(self, coord: tuple):
        return coord[0] in self.get_range_x() and coord[1] in self.get_range_y()


    def interact(self, coord: tuple):
        abs_coord = (coord[0] - self.pos[0], coord[1] - self.pos[1])

        if isinstance(self.obj, pool.Pool):
            x = int(abs_coord[0] / (self.size[0] / self.obj.cells_x))
            y = int(abs_coord[1] / (self.size[1] / self.obj.cells_x))
            self.obj.map[y][x] = self.obj.opp[self.obj.map[y][x]]

        elif isinstance(self.obj, controlbar.ControlBar):
            for lbutton in self.obj.objects:
                if lbutton.is_in_range(abs_coord):
                    print("Button [{}] clicked".format(lbutton.obj.label))
                    lbutton.obj.action()
