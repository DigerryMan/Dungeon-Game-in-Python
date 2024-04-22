from config import *
from entities.mobs.alpha_maggot import AlphaMaggot
from entities.mobs.fly import Fly
from entities.mobs.friendly_ghost import FriendlyGhost
from entities.mobs.ghost import Ghost
from entities.mobs.maggot import Maggot
from entities.mobs.slime import Slime
from entities.mobs.wanderer import Wanderer
from .room_types import rooms, special_rooms
from .block import *
from .destructable_block import *
from .shop_stuff.shop_stand import *
from .door import *
from .wall import *
from .chest import *
from items.lootable_item import LootableItem
from entities.player.player import *
from entities.enemy import *
from entities.mobs.legs import *
from entities.mobs.parasite import *

class Room():    
    def __init__(self, room_type, game, doors_to_spawn:Directions):
        if room_type in special_rooms:
            self.room = special_rooms[room_type]
        else:
            self.room = rooms[room_type]

        self.game = game
        self.player = game.player
        self.room_cleared = False
        self.drawn_once = False
        self.doors_to_spawn = doors_to_spawn

        self.room_background = {}

        self.select_graphics()

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
    
    def remove_item(self, item:LootableItem):
        self.items.remove(item)

    def remove_block(self, block:Block):
        self.blocks.remove(block)

    def generate_room(self, entry_direction:Directions):
        if not self.drawn_once:
            doors_positions = self.get_doors_positions()

            for y, row in enumerate(self.room):
                for x, col in enumerate(row):
                    if col == 'C':
                        self.chest = Chest(self.game, x, y, "small")

                    elif col == 'B':
                        self.blocks.append(Block(self.game, x, y))

                    elif col == 'D':
                        self.blocks.append(DestructableBlock(self.game, x, y))

                    elif col == 's':
                        self.blocks.append(ShopStand(self.game, x + .5, y + .5))

                    if not self.room_cleared:
                        if col == 'E':
                            self.enemies.append(Wanderer(self.game, x, y))
                        elif col == 'L':
                            self.enemies.append(Legs(self.game, x, y))
                        elif col == 'P':
                            self.enemies.append(Parasite(self.game, x, y))
                        elif col == 'M':
                            self.enemies.append(Maggot(self.game, x, y))
                        elif col == 'A':
                            self.enemies.append(AlphaMaggot(self.game, x, y))
                        elif col == 'F':
                            self.enemies.append(Fly(self.game, x, y))
                        elif col == 'S':
                            self.enemies.append(Slime(self.game, x, y))
                        elif col == 'G':
                            self.enemies.append(Ghost(self.game, x, y))

            for (y, x) in doors_positions:
                if(y == 0):
                    self.doors.append(Door(self.game, x, y, Directions.UP))
                elif(y == self.game.settings.MAP_HEIGHT - 1):
                    self.doors.append(Door(self.game, x, y, Directions.DOWN))
                elif(x == 0):
                    self.doors.append(Door(self.game, x, y, Directions.LEFT))
                elif(x == self.game.settings.MAP_WIDTH - 1):
                    self.doors.append(Door(self.game, x, y, Directions.RIGHT))

            #top wall
            x = 0
            while x < self.game.settings.MAP_WIDTH:
                if((0, x + 0.5) not in doors_positions):
                    self.walls.append(Wall(self.game, x, 0))
                else:
                    self.walls.append(Wall(self.game, x - 0.5, 0))
                    self.walls.append(Wall(self.game, x + 1.5, 0))
                    x += 1

                x += 1

            #bottom wall
            x = 0
            while x < self.game.settings.MAP_WIDTH:
                if((self.game.settings.MAP_HEIGHT - 1, x + 0.5) not in doors_positions):
                    self.walls.append(Wall(self.game, x, self.game.settings.MAP_HEIGHT - 1))
                else:
                    self.walls.append(Wall(self.game, x - 0.5, self.game.settings.MAP_HEIGHT - 1))
                    self.walls.append(Wall(self.game, x + 1.5, self.game.settings.MAP_HEIGHT - 1))
                    x += 1

                x += 1
            
            #left wall
            y = 0
            while y < self.game.settings.MAP_HEIGHT:
                if((y, 0) not in doors_positions):
                    self.walls.append(Wall(self.game, 0, y))

                y += 1

            #right wall
            y = 0
            while y < self.game.settings.MAP_HEIGHT:
                if((y, self.game.settings.MAP_WIDTH - 1) not in doors_positions):
                    self.walls.append(Wall(self.game, self.game.settings.MAP_WIDTH - 1, y))

                y += 1

        self.spawn_player(entry_direction)
        self.player.spawn_pets()
        self.drawn_once = True
        
    
    def spawn_player(self, entry_direction):
        if entry_direction == Directions.UP:
            self.player.set_rect_position(self.player.rect.x, (self.game.settings.MAP_HEIGHT - 2) * self.game.settings.TILE_SIZE)

        elif entry_direction == Directions.DOWN:
            self.player.set_rect_position(self.player.rect.x, self.game.settings.TILE_SIZE)

        elif entry_direction == Directions.LEFT:
            self.player.set_rect_position((self.game.settings.MAP_WIDTH - 2) * self.game.settings.TILE_SIZE, self.player.rect.y)

        elif entry_direction == Directions.RIGHT:
            self.player.set_rect_position(self.game.settings.TILE_SIZE, self.player.rect.y)

        elif entry_direction == Directions.CENTER:
            self.player.set_rect_position((self.game.settings.MAP_WIDTH / 2 - 0.5) * self.game.settings.TILE_SIZE, (self.game.settings.MAP_HEIGHT / 2 - 0.5) * self.game.settings.TILE_SIZE)


    def get_doors_positions(self):
        doors_positions = []
        for i in range(len(self.doors_to_spawn)):
            if self.doors_to_spawn[i] == Directions.UP:
                doors_positions.append((0, self.game.settings.MAP_WIDTH / 2 - 0.5))

            elif self.doors_to_spawn[i] == Directions.DOWN:
                doors_positions.append((self.game.settings.MAP_HEIGHT - 1, self.game.settings.MAP_WIDTH / 2 - 0.5))

            elif self.doors_to_spawn[i] == Directions.LEFT:
                doors_positions.append((self.game.settings.MAP_HEIGHT / 2 - 0.5, 0))

            elif self.doors_to_spawn[i] == Directions.RIGHT:
                doors_positions.append((self.game.settings.MAP_HEIGHT / 2 - 0.5, self.game.settings.MAP_WIDTH - 1))
        
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
    

    def select_graphics(self):
        #if self.room == special_rooms["shop"]:
        #    print("shop")
        self.room_background["background_image"] = self.game.image_loader.get_image("shop_room")
        self.room_background["shading"] = self.game.image_loader.get_image("shading")


    def draw(self, screen):
        screen.blit(self.room_background["background_image"], (-self.game.settings.WIN_WIDTH * 0.04, -self.game.settings.WIN_HEIGHT * 0.04))
        screen.blit(self.room_background["shading"], (-self.game.settings.WIN_WIDTH * 0.04, -self.game.settings.WIN_HEIGHT * 0.04))