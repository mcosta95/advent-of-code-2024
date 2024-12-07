from enum import Enum


class DIRECTIONS(Enum):

    UP_LEFT = (-1, -1)
    UP = (-1, 0)
    UP_RIGHT = (-1, 1)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    DOWN_LEFT = (1, -1)
    DOWN = (1, 0)
    DOWN_RIGHT = (1, 1)

    @classmethod
    def all_directions(cls):
        """Returns all directions as a list of tuples."""
        return [direction.value for direction in cls]

    @classmethod
    def diagonal_directions(cls):
        """Returns only diagonal directions as a list of tuples."""
        return [cls.UP_LEFT.value, cls.UP_RIGHT.value, cls.DOWN_LEFT.value, cls.DOWN_RIGHT.value]
    
    @classmethod
    def arrow_directions(cls):
        return {"^": cls.UP.value, ">": cls.RIGHT.value, "v": cls.DOWN.value, "<": cls.LEFT.value}

