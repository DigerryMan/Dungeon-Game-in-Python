from config import *
from .room_types import rooms
from .block import *
from entities.player import *

class Room():    
    def __init__(self, room_type):
        self.room = rooms[room_type]

    def draw_room(self, game):
        for i, row in enumerate(self.room):
            for j, col in enumerate(row):
                if col == '#':
                    Block(game, j, i)

                if col == 'P':
                    Player(game, j, i)