import pygame

from ui import displayedobject

class ControlBar(object):
    """description of class"""

    def __init__(self, size, **kwargs):
        """
        kwargs:
            bg_color: int
            align: str [ left | center | right ]
        """
        self.size = size
        self.bg_color = kwargs.get('bg_color', 0xFFFFFF)
        self.align = kwargs.get('align', 'center')
        self.objects = list()
        self.box = pygame.Surface((size[0], size[1]))
        for content in kwargs.get('content', []):
            self.add_object(content)


    def generate(self):
        self.box.fill(self.bg_color)
        for obj in self.objects:
            self.box.blit(obj.obj.box, obj.pos)


    def add_object(self, new_object):
        if new_object.size[1] > self.size[1]:
            raise OverflowError("Button too tall for the controlbar")
        total_lenght = 0
        for obj in self.objects:
            total_lenght += obj.obj.get_width()
        total_lenght += new_object.get_width()
        if total_lenght > self.size[0]:
            raise OverflowError("Not enough width to add the button")

        if self.align == "center":
            begin = int((self.size[0] - total_lenght) / 2)
        elif self.align == "left":
            begin = 0
        elif self.align == "right":
            begin = self.size[0] - total_lenght
        else:
            raise BaseException("Align mode not handled")

        curr_length = 0
        for obj in self.objects:
            obj.pos = (begin + curr_length,
                       int(self.size[1] / 2 - obj.obj.size[1] / 2))
            curr_length += obj.obj.get_width()

        self.objects.append(displayedobject.DisplayedObject(
            new_object,
            (begin + curr_length, int(self.size[1] / 2 - new_object.size[1] / 2)),
            new_object.size))
