from enum import Enum

class Directions(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    CENTER = (0, 0)
    PLAYER = (0, 0)
    ENEMY = (0, 0)

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
    
    def get_direction_from_two_points(x1, y1, x2, y2):
        a = abs(y1 - y2)
        b = abs(x2 - x1)
        c = (a**2 + b**2)**0.5
        sin = a/c
        if sin > 0.5:
            if y1 > y2:
                return Directions.UP
            return Directions.DOWN
        elif x1 <= x2:
            return Directions.RIGHT
        return Directions.LEFT