from config import *
from .room_types import rooms, special_rooms
from .room import Room
from entities.player import *
import random
from math import inf
from collections import deque

class Map():
    def __init__(self, game, player:Player):
        self.room_map = [[None for _ in range(15)] for _ in range(15)]
        self.game = game
        self.player = player
        self.current_position = [0, 0]
        self.map_scheme = self.create_map_scheme()
        self._generate_rooms()


    def create_map_scheme(self):
        #setting row, col for starting room
        row = 7
        col = 7

        self.current_position = [row, col]
        satisfied = False

        while not satisfied:
            arr = [[0 for _ in range(15)] for _ in range(15)]
            arr[row][col] = 1

            self.create_map_shape(arr, row, col)

            distance_array = [[-inf for _ in range(15)] for _ in range(15)]
            distance_array[row][col] = 0

            self.fill_distances(arr, distance_array, row, col)

            row_max = 0
            col_max = 0

            for row in range(len(distance_array)):
                for col in range(len(distance_array[row])):
                    if distance_array[row][col] > distance_array[row_max][col_max]:
                        row_max, col_max = row, col
            
            distance_array[row_max][col_max] = 0
            satisfied, key_rooms = self.check_if_map_valid(distance_array, row_max, col_max)

        shop_row, shop_col = key_rooms["shop"]
        boss_row, boss_col = key_rooms["boss"]
        start_row, start_col = key_rooms["start"]

        distance_array[shop_row][shop_col] = 'S'
        distance_array[boss_row][boss_col] = 'B'
        distance_array[start_row][start_col] = 'T'

        return distance_array

    def _generate_rooms(self):
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

                    if new_row >= 0 and new_row < 15 and new_col >= 0 and new_col < 15 and self.map_scheme[new_row][new_col] != -inf:
                        doors_to_spawn.append(door_directions[i])

                if self.map_scheme[row][col] == 'S':
                    self.room_map[row][col] = Room("shop", self.player, doors_to_spawn)

                elif self.map_scheme[row][col] == 'B':
                    self.room_map[row][col] = Room("boss", self.player, doors_to_spawn)

                elif self.map_scheme[row][col] == 'T':
                    self.room_map[row][col] = Room("start", self.player, doors_to_spawn)
                    self.current_position = [row, col]

                else:
                    room_random_type = random.randint(0, len(rooms) - 1)
                    self.room_map[row][col] = Room(room_random_type, self.player, doors_to_spawn)


    def render_initial_room(self):
        row, col = self.current_position

        room = self.room_map[row][col]
        room.generate_room(self.game, Directions.CENTER)


    def render_next_room(self, direction:Directions):
        self._change_position_on_map(direction)
        row, col = self.current_position

        room = self.room_map[row][col]
        room.generate_room(self.game, direction)
        

    def get_current_room(self):
        return self.room_map[self.current_position[0]][self.current_position[1]]


    def _change_position_on_map(self, direction:Directions):
        if direction == Directions.UP:
            self.current_position[0] -= 1

        elif direction == Directions.DOWN:
            self.current_position[0] += 1

        elif direction == Directions.LEFT:
            self.current_position[1] -= 1

        elif direction == Directions.RIGHT:
            self.current_position[1] += 1


    def set_room_cleared(self):
        x, y = self.current_position
        self.room_map[x][y].set_room_cleared()


    def create_map_shape(self, arr, row_, col_):
        room_cnt = 1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        row, col = row_, col_
        while room_cnt <= ROOM_NUMBER:
            arr[row][col] = 1
            room_cnt += 1

            d_row, d_col = random.choice(directions)
            row, col = row + d_row, col + d_col

            if row < 0 or col < 0 or row >= 15 or col >= 15:
                row, col = row - d_row, col - d_col

            while arr[row][col] == 1:
                d_row, d_col = random.choice(directions)
                row, col = row + d_row, col + d_col
                if row < 0 or col < 0 or row >= 15 or col >= 15:
                    row, col = row - d_row, col - d_col


    def fill_distances(self, arr, distance_array, row, col):
        q = deque()
        q.append([row, col])
        visited = [[False for _ in range(15)] for _ in range(15)]
        visited[row][col] = True

        d_row = [0, 0, 1, -1]
        d_col = [1, -1, 0, 0]

        while len(q) > 0:
            row, col = q.popleft()

            for i in range(4):
                new_row = row + d_row[i]
                new_col = col + d_col[i]

                if new_row >= 0 and new_row < 15 and new_col >= 0 and new_col < 15 and not visited[new_row][new_col] and arr[new_row][new_col] == 1:
                    distance_array[new_row][new_col] = distance_array[row][col] + 1
                    q.append([new_row, new_col])
                    visited[new_row][new_col] = True


    def check_if_map_valid(self, arr, row_, col_):
        q = deque()
        q.append([row_, col_])
        visited = [[False for _ in range(15)] for _ in range(15)]
        visited[row_][col_] = True

        d_row = [0, 0, 1, -1]
        d_col = [1, -1, 0, 0]

        furthest_distance = 0

        while len(q) > 0:
            row, col = q.popleft()

            for i in range(4):
                new_row = row + d_row[i]
                new_col = col + d_col[i]

                if new_row >= 0 and new_row < 15 and new_col >= 0 and new_col < 15 and not visited[new_row][new_col] and arr[new_row][new_col] >= 0:
                    arr[new_row][new_col] = arr[row][col] + 1
                    furthest_distance = max(furthest_distance, arr[new_row][new_col])
                    q.append([new_row, new_col])
                    visited[new_row][new_col] = True
            
        key_rooms = {
            "start" : None,
            "shop"  : None,
            "boss"  : None
        }   
        
        for row in range(len(arr)):
            for col in range(len(arr[row])):
                if arr[row][col] == 0:
                    neighbors = 0
                    for i in range(4):
                        new_row = row + d_row[i]
                        new_col = col + d_col[i]

                        if new_row >= 0 and new_row < 15 and new_col >= 0 and new_col < 15 and arr[new_row][new_col] > 0:
                            neighbors += 1

                    if neighbors == 1:
                        key_rooms["start"] = [row, col]

                    else:
                        return False, key_rooms
                
                elif arr[row][col] == furthest_distance:
                    neighbors = 0
                    for i in range(4):
                        new_row = row + d_row[i]
                        new_col = col + d_col[i]

                        if new_row >= 0 and new_row < 15 and new_col >= 0 and new_col < 15 and arr[new_row][new_col] > 0:
                            neighbors += 1

                    if neighbors == 1:
                        key_rooms["boss"] = [row, col]

                elif arr[row][col] >= furthest_distance // 2 and arr[row][col] <= furthest_distance - 1:
                    neighbors = 0
                    for i in range(4):
                        new_row = row + d_row[i]
                        new_col = col + d_col[i]

                        if new_row >= 0 and new_row < 15 and new_col >= 0 and new_col < 15 and arr[new_row][new_col] > 0:
                            neighbors += 1

                    if neighbors == 1:
                        key_rooms["shop"] = [row, col]

        if key_rooms["start"] is None or key_rooms["shop"] is None or key_rooms["boss"] is None:
            return False, key_rooms

        return True, key_rooms