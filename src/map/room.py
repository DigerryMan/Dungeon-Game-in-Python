import random
from collections import deque
from entities.mobs.alpha_maggot import AlphaMaggot
from entities.mobs.boss.forsaken.forsaken import Forsaken
from entities.mobs.boss.monstro.monstro import Monstro
from entities.mobs.boss.satan.satan import Satan
from entities.mobs.fly import Fly
from entities.mobs.ghost import Ghost
from entities.mobs.legs import Legs
from entities.mobs.maggot import Maggot
from entities.mobs.parasite import Parasite
from entities.mobs.slime import Slime
from entities.mobs.wanderer import Wanderer
from map.shop_stand import ShopStand
from map.trap_door import TrapDoor
from map.treasure_block import TreasureBlock
from utils.directions import Directions
from .room_types import rooms, special_rooms
from .block import Block
from .door import Door
from .wall import Wall
from .chest import Chest
from items.lootable_item import LootableItem
from entities.enemy import Enemy
from .destructable_block import DestructableBlock

class Room():    
    def __init__(self, room_type, game, doors_to_spawn:Directions, level):
        if room_type in special_rooms:
            self.room = special_rooms[room_type]
        else:
            self.room = rooms[room_type]

        self.game = game
        self.player = game.player
        self.level = level
        self.room_type = room_type
        self.is_cleared = False
        self.drawn_once = False
        self.doors_to_spawn = doors_to_spawn

        self.room_graphics = {}
        self.select_graphics()

        self.crucial_positions = []
        self.mob_spawn_positions = []
        self.mobs_amount = game.difficulty * 2 + level // 2 + 2
        self.well_generated = False

        self.doors = []
        self.chest:Chest = None
        self.enemies = []
        self.blocks = []
        self.shop_stands = []
        self.walls = []
        self.items = []
        self.trap_door:TrapDoor = None

    def get_objects(self):
        return {
            "doors": self.doors,
            "chest": self.chest,
            "enemies": self.enemies,
            "blocks": self.blocks,
            "shop_stands": self.shop_stands,
            "walls": self.walls,
            "items": self.items,
            "trap_door": self.trap_door
        }
    
    def remove_item(self, item:LootableItem):
        self.items.remove(item)

    def remove_block(self, block:Block):
        self.blocks.remove(block)

    def remove_shop_stand(self, shop_stand:ShopStand):
        self.shop_stands.remove(shop_stand)

    def generate_room(self, entry_direction:Directions):
        if not self.drawn_once:
            random_block_density_factor = random.uniform(0.05, 0.1)
            while not self.well_generated:
                doors_positions = self.get_doors_positions()
                room_map = [[self.room[y][x] for x in range(len(self.room[y]))] for y in range(len(self.room))]

                for y, row in enumerate(self.room):
                    for x, col in enumerate(row):
                        if col == 'C' and not self.chest and random.uniform(0, 1) < 0.60: # 60% chance to actually spawn a chest
                            rand = random.uniform(0, 1)
                            if rand < 0.45:
                                self.chest = Chest(self.game, x, y, "small")
                            elif rand < 0.80:
                                self.chest = Chest(self.game, x, y, "medium")
                            else:
                                self.chest = Chest(self.game, x, y, "large")

                        elif col == 'B':
                            if random.uniform(0, 1) < 0.9:
                                self.blocks.append(Block(self.game, x, y))
                            else:
                                self.blocks.append(TreasureBlock(self.game, x, y))

                        elif col == 'D':
                            self.blocks.append(DestructableBlock(self.game, x, y))

                        elif col == 's':
                            self.shop_stands.append(ShopStand(self.game, x + .5, y + .5))

                        elif col == 'T':
                            self.trap_door = TrapDoor(self.game, x + 1, y)

                        elif col == 'E':
                            self.mob_spawn_positions.append((y, x))
                            self.crucial_positions.append((y, x))

                        else:
                            if self.room_type not in special_rooms and col != "#" and random.uniform(0, 1) < random_block_density_factor: # chance of random block that wasn't planned
                                if random.uniform(0, 1) < 0.5:
                                    self.blocks.append(DestructableBlock(self.game, x, y))
                                    room_map[y][x] = 'D'
                                else:
                                    self.blocks.append(Block(self.game, x, y))
                                    room_map[y][x] = 'B'


                if self.check_if_room_well_generated(room_map) == False:
                    self.crucial_positions.clear()
                    self.mob_spawn_positions.clear()
                    self.doors = []
                    self.chest:Chest = None
                    self.enemies = []
                    self.blocks = []
                    self.walls = []
                    self.items = []
                    self.trap_door:TrapDoor = None
                    self.game.clear_sprites()
                    continue

                self.well_generated = True

                for (y, x) in doors_positions:
                    direction = None

                    if(y == 0):
                        direction = Directions.UP
                    elif(y == self.game.settings.MAP_HEIGHT - 1):
                        direction = Directions.DOWN
                    elif(x == 0):
                        direction = Directions.LEFT
                    elif(x == self.game.settings.MAP_WIDTH - 1):
                        direction = Directions.RIGHT

                    if self.room_type == "boss":
                        self.doors.append(Door(self.game, x, y, direction, "boss_door"))
                    else:
                        current_position = self.game.map.current_position
                        neighbor_room = self.game.map.room_map[current_position[0] + direction.value[0]][current_position[1] + direction.value[1]]
                        if neighbor_room.room_type == "boss":
                            self.doors.append(Door(self.game, x, y, direction, "boss_door"))
                        else:
                            self.doors.append(Door(self.game, x, y, direction))
                    
                self.spawn_outer_walls(doors_positions)

                for door in self.doors:
                    if door.direction == entry_direction.reverse(): #if the door is the one the player used to enter the room
                        door.animate_closing()

                self.room = room_map
                self.spawn_mobs()
                """print("Room layout:")
                for row in self.room:
                    print(' '.join(row))

                print("\n")"""
                

        self.spawn_player(entry_direction)
        self.player.spawn_pets()
        self.drawn_once = True

        if self.room_type == "boss" and not self.is_cleared:
            self.game.sound_manager.stop_with_fadeout("basementLoop", 1000)
            self.game.menu.display_boss_intro(self.enemies[0])
            self.game.sound_manager.play("bossEnter")
            self.game.sound_manager.play_with_fadein("bossFight", 1000, looped=True)
        
    def spawn_outer_walls(self, doors_positions):
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
    
    def spawn_player(self, entry_direction):
        if entry_direction == Directions.UP:
            self.player.rect.center = (self.game.settings.WIN_WIDTH // 2, (self.game.settings.MAP_HEIGHT - 2) * self.game.settings.TILE_SIZE + self.game.settings.PLAYER_SIZE * 0.9)

        elif entry_direction == Directions.DOWN:
            self.player.rect.center = (self.game.settings.WIN_WIDTH // 2, self.game.settings.TILE_SIZE * 1.1)

        elif entry_direction == Directions.LEFT:
            self.player.set_rect_position((self.game.settings.MAP_WIDTH - 2) * self.game.settings.TILE_SIZE + (self.game.settings.TILE_SIZE - self.game.settings.PLAYER_SIZE),
                                          self.player.rect.y)

        elif entry_direction == Directions.RIGHT:
            self.player.set_rect_position(self.game.settings.TILE_SIZE - (self.game.settings.TILE_SIZE - self.game.settings.PLAYER_SIZE),
                                          self.player.rect.y)

        elif entry_direction == Directions.CENTER:
            self.player.rect.center = (self.game.settings.WIN_WIDTH // 2, self.game.settings.WIN_HEIGHT // 2)

    def spawn_mobs(self):
        self.mobs_amount = min(self.mobs_amount, len(self.mob_spawn_positions))
        self.mob_spawn_positions = random.sample(self.mob_spawn_positions, self.mobs_amount)

        mobs = [Legs, Parasite, AlphaMaggot, Fly, Ghost, Maggot, Slime, Wanderer]
        index = random.randint(0, len(mobs) - 1)

        if self.room_type == "boss":
            #self.enemies.append(Monstro(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
            #self.enemies.append(Satan(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
            self.enemies.append(Forsaken(self.game, self.mob_spawn_positions[0][1], self.mob_spawn_positions[0][0]))
            return

        for (y, x) in self.mob_spawn_positions:
            new_mob = mobs[index]
            self.enemies.append(new_mob(self.game, x, y))
            index = random.randint(0, len(mobs) - 1)
            break # ADDED FOR ONLY 1 MOB TO SPAWN

    def spawn_mob(self, mob_class, x, y):
        self.enemies.append(mob_class(self.game, x, y))

    def get_doors_positions(self):
        doors_positions = []
        for i in range(len(self.doors_to_spawn)):
            if self.doors_to_spawn[i] == Directions.UP:
                doors_positions.append((0, self.game.settings.MAP_WIDTH / 2 - 0.5))
                self.crucial_positions.append((1, self.game.settings.MAP_WIDTH // 2 - 1))
                self.crucial_positions.append((1, self.game.settings.MAP_WIDTH // 2))

            elif self.doors_to_spawn[i] == Directions.DOWN:
                doors_positions.append((self.game.settings.MAP_HEIGHT - 1, self.game.settings.MAP_WIDTH / 2 - 0.5))
                self.crucial_positions.append((self.game.settings.MAP_HEIGHT - 2, self.game.settings.MAP_WIDTH // 2 - 1))
                self.crucial_positions.append((self.game.settings.MAP_HEIGHT - 2, self.game.settings.MAP_WIDTH // 2))

            elif self.doors_to_spawn[i] == Directions.LEFT:
                doors_positions.append((self.game.settings.MAP_HEIGHT / 2 - 0.5, 0))
                self.crucial_positions.append((self.game.settings.MAP_HEIGHT // 2, 1))

            elif self.doors_to_spawn[i] == Directions.RIGHT:
                doors_positions.append((self.game.settings.MAP_HEIGHT / 2 - 0.5, self.game.settings.MAP_WIDTH - 1))
                self.crucial_positions.append((self.game.settings.MAP_HEIGHT // 2, self.game.settings.MAP_WIDTH - 2))
        
        return doors_positions

    def set_room_cleared(self):
        self.update_player_rooms_cleared()
        self.is_cleared = True
        self.enemies.clear()

        for door in self.doors:
            door.open()

        if self.chest and not self.chest.is_open:
            items_dropped = self.chest.open()
            for item in items_dropped:
                self.items.append(item)

        if self.trap_door:
            self.trap_door.open()

        if self.room_type == "boss":
            self.game.sound_manager.stop_with_fadeout("bossFight", 2000)
            self.game.sound_manager.play_with_fadein("basementLoop", 2000, looped=True)
            
    def update_player_rooms_cleared(self):
        if not self.is_cleared and self.room_type != "start" and self.room_type != "shop":
            self.game.player.update_rooms_cleared()

    def get_block_layout(self):
        return self.room
    
    def select_graphics(self):
        if self.room_type == "start" and self.level == 1:
            self.room_graphics["controls"] = self.game.image_loader.get_image("controls")

        if self.level <= 1:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("basement" + str(random.randint(1, 4)))

        elif self.level <= 2:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("cave" + str(random.randint(1, 5)))

        elif self.level <= 3:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("catacombs" + str(random.randint(1, 3)))

        elif self.level <= 4:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("necropolis1")

        elif self.level <= 5:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("depths" + str(random.randint(1, 3)))

        elif self.level <= 6:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("bluewomb" + str(random.randint(1, 3)))

        elif self.level <= 7:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("womb" + str(random.randint(1, 4)))

        if self.room == special_rooms["shop"]:
            self.room_graphics["background_image"] = self.game.image_loader.get_image("shop_room")
            
        self.room_graphics["shading"] = self.game.image_loader.get_image("shading")


    def draw(self, screen):
        screen.blit(self.room_graphics["background_image"], (-self.game.settings.WIN_WIDTH * 0.04, -self.game.settings.WIN_HEIGHT * 0.04))
        if self.room_type == "start" and self.level == 1:
            controls_rect = self.room_graphics["controls"].get_rect()
            screen.blit(self.room_graphics["controls"], ((self.game.settings.WIN_WIDTH - controls_rect.width) // 2.1, (self.game.settings.WIN_HEIGHT - controls_rect.height) // 2))

        self.game.doors.draw(screen)
        self.game.blocks.draw(screen)
        self.game.chest.draw(screen)
        self.game.items.draw(screen)
        self.game.trap_door.draw(screen)

        for shop_stand in self.shop_stands:
            shop_stand.draw()

        to_be_sorted = self.game.entities.sprites() + self.game.items.sprites()
        
        sprite_list = sorted(to_be_sorted, key=lambda sprite: sprite._layer)
        for sprite in sprite_list:
            if isinstance(sprite, Enemy):
                sprite.draw_additional_images(screen)
            screen.blit(sprite.image, sprite.rect)
            

        screen.blit(self.room_graphics["shading"], (-self.game.settings.WIN_WIDTH * 0.04, -self.game.settings.WIN_HEIGHT * 0.04))

    def check_if_room_well_generated(self, room_map):
        row, col = self.crucial_positions[0]
        width = len(room_map[0])
        height = len(room_map)
        q = deque()
        q.append([row, col])
        visited = [[False for _ in range(width)] for _ in range(height)]

        d_row = [0, 0, 1, -1]
        d_col = [1, -1, 0, 0]

        while len(q) > 0:
            row, col = q.popleft()

            for i in range(4):
                new_row = row + d_row[i]
                new_col = col + d_col[i]

                if new_row > 0 and new_row < height - 1 and new_col > 0 and new_col < width - 1 and not visited[new_row][new_col] and room_map[new_row][new_col] not in ['B', 'C']:
                    if (new_row, new_col) not in self.crucial_positions:
                        q.append([new_row, new_col])
                        visited[new_row][new_col] = True

                    elif room_map[new_row][new_col] != 'D':
                        q.append([new_row, new_col])
                        visited[new_row][new_col] = True

        """for row in visited:
            mapped_row = map(lambda x: '.' if x else '#', row)
            print(' '.join(mapped_row))"""

        for y, x in self.crucial_positions:
            if not visited[y][x]:
                return False
            
        return True
    