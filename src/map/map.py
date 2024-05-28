import random
from math import inf
from config import MAP_RANGE
from map.minimap import Minimap
from utils.map_generator import MapGenerator
from .room_types import rooms
from .room import Room
from entities.player.player import Player
from utils.directions import Directions

class Map():
    def __init__(self, game, player:Player, level):
        self.room_map = [[None for _ in range(MAP_RANGE)] for _ in range(MAP_RANGE)]
        self.game = game
        self.player = player
        self.level = level
        self.current_position = None
        self.map_scheme = MapGenerator.create_map_scheme()
        self.generate_rooms()
        self.minimap = Minimap(self)

    def generate_rooms(self):
        for row in range(len(self.map_scheme)):
            for col in range(len(self.map_scheme[row])):
                if self.map_scheme[row][col] == -inf:
                    continue

                d_row = [0, 0, 1, -1]
                d_col = [1, -1, 0, 0]
                door_directions = [Directions.RIGHT, Directions.LEFT, Directions.DOWN, Directions.UP]

                doors_to_spawn = []

                for i in range(4):
                    new_row = row + d_row[i]
                    new_col = col + d_col[i]

                    if new_row >= 0 and new_row < MAP_RANGE and new_col >= 0 and new_col < MAP_RANGE and self.map_scheme[new_row][new_col] != -inf:
                        doors_to_spawn.append(door_directions[i])

                if self.map_scheme[row][col] == 'S':
                    self.room_map[row][col] = Room("shop", self.game, doors_to_spawn, self.level)

                elif self.map_scheme[row][col] == 'B':
                    self.room_map[row][col] = Room("boss", self.game, doors_to_spawn, self.level)

                elif self.map_scheme[row][col] == 'T':
                    self.room_map[row][col] = Room("start", self.game, doors_to_spawn, self.level)
                    self.current_position = [row, col]

                else:
                    room_random_type = random.randint(0, len(rooms) - 1)
                    self.room_map[row][col] = Room(room_random_type, self.game, doors_to_spawn, self.level)


    def render_initial_room(self):
        row, col = self.current_position

        room = self.room_map[row][col]
        room.generate_room(Directions.CENTER)
        self.minimap.update_minimap()


    def render_next_room(self, direction:Directions):
        self.change_position_on_map(direction)
        row, col = self.current_position

        room = self.room_map[row][col]
        room.generate_room(direction)
        self.minimap.update_minimap()
        
    def change_position_on_map(self, direction:Directions):
        if direction == Directions.UP:
            self.current_position[0] -= 1

        elif direction == Directions.DOWN:
            self.current_position[0] += 1

        elif direction == Directions.LEFT:
            self.current_position[1] -= 1

        elif direction == Directions.RIGHT:
            self.current_position[1] += 1

    def get_current_room(self):
        return self.room_map[self.current_position[0]][self.current_position[1]]


    def set_room_cleared(self):
        x, y = self.current_position
        room = self.room_map[x][y]
        if not room.is_cleared:
            room.set_room_cleared()

    def draw_minimap(self, screen):
        self.minimap.draw(screen)