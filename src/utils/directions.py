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
        
        return self

    def rotate_clockwise(self):
        if self == Directions.UP:
            return Directions.RIGHT
        elif self == Directions.RIGHT:
            return Directions.DOWN
        elif self == Directions.DOWN:
            return Directions.LEFT
        elif self == Directions.LEFT:
            return Directions.UP
        
        return self
    
    def rotate_counter_clockwise(self):
        if self == Directions.UP:
            return Directions.LEFT
        elif self == Directions.LEFT:
            return Directions.DOWN
        elif self == Directions.DOWN:
            return Directions.RIGHT
        elif self == Directions.RIGHT:
            return Directions.UP
        
        return self