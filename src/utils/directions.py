from enum import Enum, auto, unique

@unique
class Directions(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()
    PLAYER = auto()
    ENEMY = auto()

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
    
    def get_axis_tuple(self):
        if self == Directions.UP or self == Directions.DOWN:
            return ('y', 1)
        elif self == Directions.LEFT or self == Directions.RIGHT:
            return ('x', 0)
        
        return None