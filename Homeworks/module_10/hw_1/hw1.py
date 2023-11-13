"""
Vasya implemented nonoptimal Enum classes.
Remove duplications in variables declarations using metaclasses.

from enum import Enum

class ColorsEnum(Enum):
    RED = "RED"
    BLUE = "BLUE"
    ORANGE = "ORANGE"
    BLACK = "BLACK"


class SizesEnum(Enum):
    XL = "XL"
    L = "L"
    M = "M"
    S = "S"
    XS = "XS"

"""

class SimplifiedEnum(type):
    def __new__(cls, name, bases, dct):
        cls_instance = super().__new__(cls, name, bases, dct)
        [setattr(cls_instance, key, key) for key in dct.get("_" + name + "__keys")]
        return cls_instance


class ColorsEnum(metaclass=SimplifiedEnum):
    __keys = ("RED", "BLUE", "ORANGE", "BLACK")


class SizesEnum(metaclass=SimplifiedEnum):
    __keys = ("XL", "L", "M", "S", "XS")


assert ColorsEnum.RED == "RED"
assert SizesEnum.XL == "XL"
