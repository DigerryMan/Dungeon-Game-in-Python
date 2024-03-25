from config import *
from .room_types import rooms
from .block import *
from entities.player import *
from entities.enemy import *

class Room():    
    def __init__(self, room_type, player:Player):
        self.room = rooms[room_type]
        self.player = player

    def draw_room(self, game):
        for i, row in enumerate(self.room):
            for j, col in enumerate(row):
                if col == '#':
                    Block(game, j, i)

                if col == 'E':
                    Enemy(game, j, i)
                    
                if col == 'P':
                    self.player.set_position(j,i)

                
