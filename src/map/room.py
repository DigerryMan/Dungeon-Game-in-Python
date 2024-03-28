from config import *
from entities.mobs.alpha_maggot import AlphaMaggot
from entities.mobs.fly import Fly
from entities.mobs.ghost import Ghost
from entities.mobs.maggot import Maggot
from entities.mobs.slime import Slime
from .room_types import rooms, special_rooms
from .block import *
from .door import *
from .wall import *
from .chest import *
from .lootables.lootable_item import Lootable_item
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
        self.drawn_once = False
        self.doors_to_spawn = doors_to_spawn

        self.doors = []
        self.chest:Chest = None
        self.enemies = []
        self.blocks = []
        self.walls = []
        self.items = []

    def get_objects(self):
        return {
            "doors": self.doors,
            "chest": self.chest,
            "enemies": self.enemies,
            "blocks": self.blocks,
            "walls": self.walls,
            "items": self.items
        }
    
    def remove_item(self, item:Lootable_item):
        self.items.remove(item)

    def generate_room(self, game, entry_direction:Directions):
        if not self.drawn_once:
            doors_positions = self.get_doors_positions()
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
                        self.walls.append(Wall(game, x, y))

                    elif col == 'C':
                        self.chest = Chest(game, x, y, "medium")

                    elif col == 'B':
                        self.blocks.append(Block(game, x, y))

                    if not self.room_cleared:
                        if col == 'E':
                            self.enemies.append(Enemy(game, x, y))
                        elif col == 'L':
                            self.enemies.append(Legs(game, x, y))
                        elif col == 'P':
                            self.enemies.append(Parasite(game, x, y))
                        elif col == 'M':
                            self.enemies.append(Maggot(game, x, y))
                        elif col == 'A':
                            self.enemies.append(AlphaMaggot(game, x, y))
                        elif col == 'F':
                            self.enemies.append(Fly(game, x, y))
                        elif col == 'S':
                            self.enemies.append(Slime(game, x, y))
                        elif col == 'G':
                            self.enemies.append(Ghost(game, x, y))

        self.spawn_player(entry_direction)
        self.drawn_once = True
        
    
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
        self.enemies.clear()

        for door in self.doors:
            door.is_open = True
            door.image.fill(GREEN)

        if self.chest and not self.chest.is_open:
            self.items = self.chest.open()
    
    def get_block_layout(self):
        return self.room