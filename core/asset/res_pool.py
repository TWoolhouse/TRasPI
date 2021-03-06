from core.asset.base import Asset

__all__ = ["Pool"]

class _MetaResourcePool(type):
    def __new__(cls, name, bases, dct):
        for k,v in ((k,v) for k,v in dct.items() if k[0] != "_"):
            if not hasattr(v, "__call__") and not isinstance(v, Asset):
                raise TypeError("Only Assets or funcs plz")
        return super().__new__(cls, name, bases, dct)

    def __len__(cls) -> int:
        return sum(True for i in cls.__dict__ if isinstance(i, Asset))

    def __getitem__(cls, key: str) -> Asset:
        return getattr(cls, key)

class Pool(metaclass=_MetaResourcePool):
    pass
