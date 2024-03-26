from enum import Enum

class Directions(Enum):
    UP = "up"
    DOWN ="down"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    PLAYER = "player"

    def reverse(self):
        if self == Directions.UP:
            return Directions.DOWN
        elif self == Directions.DOWN:
            return Directions.UP
        elif self == Directions.LEFT:
            return Directions.RIGHT
        elif self == Directions.RIGHT:
            return Directions.LEFT
        

