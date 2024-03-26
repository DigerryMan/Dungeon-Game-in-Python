from config import *
from entities.mobs.maggot import Maggot
from .room_types import rooms, special_rooms
from .block import *
from .door import *
from .wall import *
from .chest import *
from entities.player import *
from entities.enemy import *
from entities.mobs.legs import *
from entities.mobs.parasite import *

class Room():    
    def __init__(self, room_type, player:Player, doors_to_spawn:Directions):
        if room_type in special_rooms:
            self.room = special_rooms[room_type]
        else:
            self.room = rooms[room_type]

        self.player = player
        self.room_cleared = False
        self.doors_to_spawn = doors_to_spawn
        self.doors = []
        self.chests = []

    def draw_room(self, game, entry_direction:Directions):
        doors_positions = self.get_doors_positions()
        self.doors = []
        for y, row in enumerate(self.room):
            for x, col in enumerate(row):
                if (y, x) in doors_positions:
                    if(y == 0):
                        self.doors.append(Door(game, x, y, Directions.UP))
                    elif(y == MAP_HEIGHT - 1):
                        self.doors.append(Door(game, x, y, Directions.DOWN))
                    elif(x == 0):
                        self.doors.append(Door(game, x, y, Directions.LEFT))
                    elif(x == MAP_WIDTH - 1):
                        self.doors.append(Door(game, x, y, Directions.RIGHT))

                elif col == '#':
                    Wall(game, x, y)

                elif col == 'C':
                    self.chests.append(Chest(game, x, y, "small"))

                elif col == 'B':
                    Block(game, x, y)

                if not self.room_cleared:
                    if col == 'E':
                        Enemy(game, x, y)
                    elif col == 'L':
                        Legs(game, x, y)
                    elif col == 'P':
                        Parasite(game, x, y)
                    elif col == 'M':
                        Maggot(game, x, y)

        self.spawn_player(entry_direction)
        print("Doors: ", len(self.doors))
        
    
    def spawn_player(self, entry_direction):
        if entry_direction == Directions.UP:
            self.player.set_rect_position(self.player.rect.x, (MAP_HEIGHT - 2)*TILE_SIZE)

        elif entry_direction == Directions.DOWN:
            self.player.set_rect_position(self.player.rect.x, 1 * TILE_SIZE)

        elif entry_direction == Directions.LEFT:
            self.player.set_rect_position((MAP_WIDTH - 2) * TILE_SIZE, self.player.rect.y)

        elif entry_direction == Directions.RIGHT:
            self.player.set_rect_position(1 * TILE_SIZE, self.player.rect.y)

        elif entry_direction == Directions.CENTER:
            self.player.set_rect_position((MAP_WIDTH / 2) * TILE_SIZE, (MAP_HEIGHT / 2) * TILE_SIZE)


    def get_doors_positions(self):
        doors_positions = []
        for i in range(len(self.doors_to_spawn)):
            if self.doors_to_spawn[i] == Directions.UP:
                doors_positions.append((0, MAP_WIDTH / 2 - 1))
                doors_positions.append((0, MAP_WIDTH / 2))

            elif self.doors_to_spawn[i] == Directions.DOWN:
                doors_positions.append((MAP_HEIGHT - 1, MAP_WIDTH / 2 - 1))
                doors_positions.append((MAP_HEIGHT - 1, MAP_WIDTH / 2))

            elif self.doors_to_spawn[i] == Directions.LEFT:
                doors_positions.append((MAP_HEIGHT / 2 - 1, 0))
                doors_positions.append((MAP_HEIGHT / 2, 0))

            elif self.doors_to_spawn[i] == Directions.RIGHT:
                doors_positions.append((MAP_HEIGHT / 2 - 1, MAP_WIDTH - 1))
                doors_positions.append((MAP_HEIGHT / 2, MAP_WIDTH - 1))
        
        return doors_positions

    def set_room_cleared(self):
        self.room_cleared = True

        for door in self.doors:
            door.is_open = True
            door.image.fill(GREEN)

        for chest in self.chests:
            chest.open()

    def draw_lootables(self, screen):
        for chest in self.chests:
            chest.update(screen)