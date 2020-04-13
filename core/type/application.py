from core.sys.attributes import Constant
from core.sys.attributes import Config
from core.asset.res_pool import Pool
from core.render.window import Window
# from core.sys.io.

__all__ = ["Application"]

class MetaApplication(type):

    def __init__(cls, name, bases, dct):
        if not issubclass(cls.var, Config):
            raise TypeError
        # core

        if not issubclass(cls.const, Constant):
            raise TypeError
        if not issubclass(cls.asset, Pool):
            raise TypeError
        if not isinstance(cls.window, Window):
            raise TypeError
        return super().__init__(name, bases, dct)

class Application(metaclass=MetaApplication):

    def interval(self, func: callable, delay: float=1, repeat: int=-1):
        """Calls func every 'delay' seconds 'repeat' number of times"""
        self._program.create_interval_func(func, delay, repeat)

    class var(Config):
        pass

    class const(Constant):
        pass

    class asset(Pool):
        pass

    window = Window()

    async def open(self):
        pass
    async def close(self):
        pass

    async def show(self):
        pass
    async def hide(self):
        pass