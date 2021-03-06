from ...vector import Vector
from ..primative import Primative

import PIL.ImageDraw

__all__ = ["Rectangle"]

class Rectangle(Primative):

    def __init__(self, pos1: Vector, pos2: Vector, outline: int=0, fill: str=None, width: int=1, zindex: int=None):
        super().__init__(zindex)
        self.pos1, self.pos2 = pos1, pos2
        self.outline, self.fill, self.width = outline, fill, width

    def copy(self):
        return self.pos1, self.pos2, self.outline, self.fill, self.width

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        image.rectangle([*self.pos1, *self.pos2], self.fill, self.outline, self.width)
