from ...vector import Vector
from ..primative import Primative
from ...asset.image import Image as AssetImage

__all__ = ["Image"]

class Image(Primative):

    def __init__(self, anchor: Vector, image: AssetImage, just_w: str='C', just_h: str=None, zindex: int=None):
        super().__init__(zindex)
        self.image, self.just_w, self.just_h = image, just_w, just_h
        self.anchor = anchor
        self._calc_pos()

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        pos = [*self.pos, *self.pos+self.image.size()]
        image.im.paste(self.image.image.im, tuple(pos))

    def copy(self):
        return self.image, self.pos, self.just_w, self.just_h

    def _calc_pos(self):
        size = self.image.size()

        try:
            self.just_w = self.just_w.upper()
            self.just_h = self.just_h.upper()
        except Exception as e:
            pass

        if self.just_w == 'R':
            off_w = self.anchor[0] - size[0]
        elif self.just_w == 'L':
            off_w = self.anchor[0]
        else:
            off_w = self.anchor[0] - (size[0] // 2)

        if self.just_h == 'B':
            off_h = self.anchor[1] + size[1]
        elif self.just_h == 'C':
            off_h = self.anchor[1] - (size[1] // 2)
        else:
            off_h = self.anchor[1]

        self.pos = Vector(off_w, off_h)
