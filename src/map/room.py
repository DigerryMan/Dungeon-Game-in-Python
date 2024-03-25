from config import *
from .room_types import rooms
from .block import *
from .door import *
from entities.player import *
from entities.enemy import *

class Room():    
    def __init__(self, room_type, player:Player):
        self.room = rooms[room_type]
        self.player = player

    def draw_room(self, game, entry_direction:str):
        for y, row in enumerate(self.room):
            for x, col in enumerate(row):
                if col == '#':
                    Block(game, x, y)

                if col == 'D':
                    #Door(game, x, y)
                    if(y == 0):
                        Door(game, x, y, 'up')
                    elif(y == MAP_HEIGHT - 1):
                        Door(game, x, y, 'down')
                    elif(x == 0):
                        Door(game, x, y, 'left')
                    elif(x == MAP_WIDTH - 1):
                        Door(game, x, y, 'right')

                if col == 'E':
                    Enemy(game, x, y)

        self.spawn_player(entry_direction)
                    
    
    def spawn_player(self, entry_direction):
        if entry_direction == 'up':
            self.player.set_rect_position(self.player.rect.x, (MAP_HEIGHT - 2)*TILE_SIZE)

        elif entry_direction == 'down':
            self.player.set_rect_position(self.player.rect.x, 1 * TILE_SIZE)

        elif entry_direction == 'left':
            self.player.set_rect_position((MAP_WIDTH - 2) * TILE_SIZE, self.player.rect.y)

        elif entry_direction == 'right':
            self.player.set_rect_position(1 * TILE_SIZE, self.player.rect.y)

        elif entry_direction == 'center':
            self.player.set_rect_position((MAP_WIDTH / 2) * TILE_SIZE, (MAP_HEIGHT / 2) * TILE_SIZE)