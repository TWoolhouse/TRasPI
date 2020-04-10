import PIL.ImageDraw
from core.vector import Vector
from core.render.primative import Primative
from core.render.element.text import Text
from core.render.element.rectangle import Rectangle

__all__ = ["TextBox"]

class TextBox(Text):  # ASK TOM

    def __init__(self, anchor, *args, line_col=0, fill=None, width=1, **kwargs):
        super().__init__(anchor, *args, *kwargs)
        self.rect = Rectangle(pos-Vector(2, 0), Vector(1, 1), line_col, fill, width)

        def render(self):
            super().render()
            self.rect.render()

        def copy(self):
            return self.anchor, self.line_col, self.fill, self.width
            
        def volatile(self):
            super().volatile()
            self._offset()

        def _offset(self):
            value = super()._offset(self.anchor)
            self.rect.pos = value - Vector(2, 0)
            self.rect.pos_2 = self.font_size() + Vector(2, 0)
            return value
