from config import *
from .room_types import rooms
from .room import Room
from entities.player import *

class Map():
    def __init__(self, game, player:Player):
        self.room_map = [[None for _ in range(6)] for _ in range(6)]
        self.game = game
        self.player = player
        self.current_position = [0, 0]
        self._generate_rooms()


    def _generate_rooms(self):
        room_type = 0
        self.current_position = [0, 0] #tu trzeba losowac pozycje startowa
        #self.room_map[0][0] = Room(room_type, self.player)
        self.room_map[0][0] = Room(0, self.player)
        self.room_map[0][1] = Room(1, self.player)
        self.room_map[1][1] = Room(2, self.player)


    def draw_initial_room(self):
        row, col = self.current_position

        room = self.room_map[row][col]
        room.draw_room(self.game, 'center')


    def draw_room(self, direction:str):
        self._change_room(direction)
        row, col = self.current_position

        room = self.room_map[row][col]
        room.draw_room(self.game, direction)


    def _change_room(self, direction:str):
        if direction == 'up':
            self.current_position[0] -= 1

        elif direction == 'down':
            self.current_position[0] += 1

        elif direction == 'left':
            self.current_position[1] -= 1

        elif direction == 'right':
            self.current_position[1] += 1

    def set_room_cleared(self):
        x, y = self.current_position
        self.room_map[x][y].set_room_cleared()