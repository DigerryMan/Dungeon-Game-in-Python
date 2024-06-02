from collections import deque
import random
from map.block import Block
from map.chest import Chest
from map.destructable_block import DestructableBlock
from map.door import Door
from map.shop_stand import ShopStand
from map.trap_door import TrapDoor
from map.treasure_block import TreasureBlock
from map.wall import Wall
from utils.directions import Directions
from .room_types import special_rooms


class RoomGenerator:
    def __init__(self, room):
        self.game = room.game
        self.room = room
        self.room_type = self.room.room_type
        self.level = self.room.level
        self.doors_to_spawn = self.room.doors_to_spawn
        self.well_generated = False

    def generate_room(self, entry_direction:Directions):
        random_block_density_factor = random.uniform(0.05, 0.1)
        while not self.well_generated:
            doors_positions = self.get_doors_positions()
            room_map = [[self.room.layout[y][x] for x in range(len(self.room.layout[y]))] for y in range(len(self.room.layout))]

            for y, row in enumerate(self.room.layout):
                for x, col in enumerate(row):
                    if col == 'C' and not self.room.chest and random.uniform(0, 1) < 0.2 + self.game.player.get_luck():
                        rand = random.uniform(0, 1)
                        if rand < 0.5 - self.game.player.get_luck():
                            self.room.chest = Chest(self.game, x, y, "small")
                        elif rand < 0.85 - self.game.player.get_luck() // 2:
                            self.room.chest = Chest(self.game, x, y, "medium")
                        else:
                            self.room.chest = Chest(self.game, x, y, "large")

                    elif col == 'B':
                        if random.uniform(0, 1) < 0.9:
                            self.room.blocks.append(Block(self.game, x, y))
                        else:
                            self.room.blocks.append(TreasureBlock(self.game, x, y))

                    elif col == 'D':
                        self.room.blocks.append(DestructableBlock(self.game, x, y))

                    elif col == 's':
                        self.room.shop_stands.append(ShopStand(self.game, x + .5, y + .5))

                    elif col == 'T':
                        self.room.trap_door = TrapDoor(self.game, x + 1, y)

                    elif col == 'E':
                        self.room.mob_spawner.mob_spawn_positions.append((y, x))
                        self.room.crucial_positions.append((y, x))

                    else:
                        if self.room_type not in special_rooms and col != "#" and random.uniform(0, 1) < random_block_density_factor: # chance of random block that wasn't planned
                            if random.uniform(0, 1) < 0.5:
                                self.room.blocks.append(DestructableBlock(self.game, x, y))
                                room_map[y][x] = 'D'
                            else:
                                self.room.blocks.append(Block(self.game, x, y))
                                room_map[y][x] = 'B'

            if self.check_if_room_well_generated(room_map) == False:
                self.room.crucial_positions.clear()
                self.room.mob_spawner.mob_spawn_positions.clear()
                self.room.doors = []
                self.room.chest = None
                self.room.enemies = []
                self.room.blocks = []
                self.room.walls = []
                self.room.items = []
                self.room.trap_door = None
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
                    self.room.doors.append(Door(self.game, x, y, direction, self.level, "boss_door"))
                else:
                    current_position = self.game.map.current_position
                    neighbor_room = self.game.map.room_map[current_position[0] + direction.value[0]][current_position[1] + direction.value[1]]
                    if neighbor_room.room_type == "boss":
                        self.room.doors.append(Door(self.game, x, y, direction, self.level, "boss_door"))
                    else:
                        if self.room_type == "shop":
                            self.room.doors.append(Door(self.game, x, y, direction, self.level, "shop_door"))
                        else:
                            self.room.doors.append(Door(self.game, x, y, direction, self.level))
                
            self.spawn_outer_walls(doors_positions)

            for door in self.room.doors:
                if door.direction == entry_direction.reverse(): #if the door is the one the player used to enter the room
                    door.animate_closing()

            self.room.layout = room_map
            self.spawn_mobs()

    def spawn_mobs(self):
        self.room.mob_spawner.spawn_mobs()

    def get_doors_positions(self):
        doors_positions = []
        for i in range(len(self.doors_to_spawn)):
            if self.doors_to_spawn[i] == Directions.UP:
                doors_positions.append((0, self.game.settings.MAP_WIDTH / 2 - 0.5))
                self.room.crucial_positions.append((1, self.game.settings.MAP_WIDTH // 2 - 1))
                self.room.crucial_positions.append((1, self.game.settings.MAP_WIDTH // 2))

            elif self.doors_to_spawn[i] == Directions.DOWN:
                doors_positions.append((self.game.settings.MAP_HEIGHT - 1, self.game.settings.MAP_WIDTH / 2 - 0.5))
                self.room.crucial_positions.append((self.game.settings.MAP_HEIGHT - 2, self.game.settings.MAP_WIDTH // 2 - 1))
                self.room.crucial_positions.append((self.game.settings.MAP_HEIGHT - 2, self.game.settings.MAP_WIDTH // 2))

            elif self.doors_to_spawn[i] == Directions.LEFT:
                doors_positions.append((self.game.settings.MAP_HEIGHT / 2 - 0.5, 0))
                self.room.crucial_positions.append((self.game.settings.MAP_HEIGHT // 2, 1))

            elif self.doors_to_spawn[i] == Directions.RIGHT:
                doors_positions.append((self.game.settings.MAP_HEIGHT / 2 - 0.5, self.game.settings.MAP_WIDTH - 1))
                self.room.crucial_positions.append((self.game.settings.MAP_HEIGHT // 2, self.game.settings.MAP_WIDTH - 2))
        
        return doors_positions
    
    def spawn_outer_walls(self, doors_positions):
        #top wall
        x = 0
        while x < self.game.settings.MAP_WIDTH:
            if((0, x + 0.5) not in doors_positions):
                self.room.walls.append(Wall(self.game, x, 0))
            else:
                self.room.walls.append(Wall(self.game, x - 0.5, 0))
                self.room.walls.append(Wall(self.game, x + 1.5, 0))
                x += 1

            x += 1

        #bottom wall
        x = 0
        while x < self.game.settings.MAP_WIDTH:
            if((self.game.settings.MAP_HEIGHT - 1, x + 0.5) not in doors_positions):
                self.room.walls.append(Wall(self.game, x, self.game.settings.MAP_HEIGHT - 1))
            else:
                self.room.walls.append(Wall(self.game, x - 0.5, self.game.settings.MAP_HEIGHT - 1))
                self.room.walls.append(Wall(self.game, x + 1.5, self.game.settings.MAP_HEIGHT - 1))
                x += 1

            x += 1
        
        #left wall
        y = 0
        while y < self.game.settings.MAP_HEIGHT:
            if((y, 0) not in doors_positions):
                self.room.walls.append(Wall(self.game, 0, y))

            y += 1

        #right wall
        y = 0
        while y < self.game.settings.MAP_HEIGHT:
            if((y, self.game.settings.MAP_WIDTH - 1) not in doors_positions):
                self.room.walls.append(Wall(self.game, self.game.settings.MAP_WIDTH - 1, y))

            y += 1
    
    def check_if_room_well_generated(self, room_map):
        row, col = self.room.crucial_positions[0]
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
                    if (new_row, new_col) not in self.room.crucial_positions:
                        q.append([new_row, new_col])
                        visited[new_row][new_col] = True

                    elif room_map[new_row][new_col] != 'D':
                        q.append([new_row, new_col])
                        visited[new_row][new_col] = True
                        
        for y, x in self.room.crucial_positions:
            if not visited[y][x]:
                return False
            
        return True