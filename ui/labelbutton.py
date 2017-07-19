import pygame

from ui import colors

class LabelButton(object):
    """description of class"""

    def __init__(self, label: str, action, **kwargs):
        """
        kwargs:
            fill: int
            font: str
            font_size: int
            font_color: tuple
            bold: bool
            italic: bool
            margin: int
            padding: int
            antialias: bool
            border: int | None
            border_color: int
        """
        self.label = label
        self.action = action
        fill = kwargs.get('fill', colors.HEXA['white'])
        font = kwargs.get('font', 'Arial')
        font_size = kwargs.get('font_size', 10)
        font_color = kwargs.get('font_color', colors.RGBA['black'])
        bold = kwargs.get('bold', False)
        italic = kwargs.get('italic', False)
        margin = kwargs.get('margin', 2)
        self.padding = kwargs.get('padding', 0)
        antialias = kwargs.get('antialias', 1)
        border = kwargs.get('border', 1)
        border_color = kwargs.get('border_color', colors.HEXA['black'])

        font = pygame.font.SysFont(
            font,
            font_size,
            bold=bold,
            italic=italic)
        text = font.render(label, antialias, font_color)
        self.size = (text.get_width() + margin * 2,
                     text.get_height() + margin * 2)
        self.box = pygame.Surface(
            (self.size[0], self.size[1]))
        if fill:
            self.box.fill(fill)
        if border:
            pygame.draw.rect(
                self.box,
                border_color,
                (0, 0, self.size[0], self.size[1]),
                border)
        self.box.blit(text, (margin, margin))


    def get_width(self):
        return self.size[0] + self.padding * 2
