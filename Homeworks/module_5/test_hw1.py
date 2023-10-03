from hw1 import *


def test():
    storage = KeyValueStorage("task1.txt")
    assert storage.name == "kek"
    assert storage['power'] == 9001
