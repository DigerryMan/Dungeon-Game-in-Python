from collections import deque
from math import inf
import random

from config import MAP_RANGE, ROOM_NUMBER


class MapGenerator():
    def __init__(self):
        pass

    @staticmethod
    def create_map_scheme():
        root_row = MAP_RANGE//2
        root_col = MAP_RANGE//2

        satisfied = False

        while not satisfied:
            arr = [[0 for _ in range(MAP_RANGE)] for _ in range(MAP_RANGE)]
            arr[root_row][root_col] = 1

            MapGenerator._create_map_shape(arr, root_row, root_col)

            distance_array = [[-inf for _ in range(MAP_RANGE)] for _ in range(MAP_RANGE)]
            distance_array[root_row][root_col] = 0

            MapGenerator._fill_distances(arr, distance_array, root_row, root_col)

            row_max = 0
            col_max = 0

            for row in range(len(distance_array)):
                for col in range(len(distance_array[row])):
                    if distance_array[row][col] > distance_array[row_max][col_max]:
                        row_max, col_max = row, col
            
            distance_array[row_max][col_max] = 0
            satisfied, key_rooms = MapGenerator._check_if_map_valid(distance_array, row_max, col_max)

        shop_row, shop_col = key_rooms["shop"]
        boss_row, boss_col = key_rooms["boss"]
        start_row, start_col = key_rooms["start"]

        distance_array[shop_row][shop_col] = 'S'
        distance_array[boss_row][boss_col] = 'B'
        distance_array[start_row][start_col] = 'T'

        return distance_array
    
    @staticmethod
    def _create_map_shape(arr, row_, col_):
        room_cnt = 1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        row, col = row_, col_
        while room_cnt <= ROOM_NUMBER:
            arr[row][col] = 1
            room_cnt += 1

            d_row, d_col = random.choice(directions)
            row, col = row + d_row, col + d_col

            if row < 0 or col < 0 or row >= MAP_RANGE or col >= MAP_RANGE:
                row, col = row - d_row, col - d_col

            while arr[row][col] == 1:
                d_row, d_col = random.choice(directions)
                row, col = row + d_row, col + d_col
                if row < 0 or col < 0 or row >= MAP_RANGE or col >= MAP_RANGE:
                    row, col = row - d_row, col - d_col

    @staticmethod
    def _fill_distances(arr, distance_array, row, col):
        q = deque()
        q.append([row, col])
        visited = [[False for _ in range(MAP_RANGE)] for _ in range(MAP_RANGE)]
        visited[row][col] = True

        d_row = [0, 0, 1, -1]
        d_col = [1, -1, 0, 0]

        while len(q) > 0:
            row, col = q.popleft()

            for i in range(4):
                new_row = row + d_row[i]
                new_col = col + d_col[i]

                if new_row >= 0 and new_row < MAP_RANGE and new_col >= 0 and new_col < MAP_RANGE and not visited[new_row][new_col] and arr[new_row][new_col] == 1:
                    distance_array[new_row][new_col] = distance_array[row][col] + 1
                    q.append([new_row, new_col])
                    visited[new_row][new_col] = True


    @staticmethod
    def _check_if_map_valid(arr, row_, col_):
        q = deque()
        q.append([row_, col_])
        visited = [[False for _ in range(MAP_RANGE)] for _ in range(MAP_RANGE)]
        visited[row_][col_] = True

        d_row = [0, 0, 1, -1]
        d_col = [1, -1, 0, 0]

        furthest_distance = 0

        while len(q) > 0:
            row, col = q.popleft()

            for i in range(4):
                new_row = row + d_row[i]
                new_col = col + d_col[i]

                if new_row >= 0 and new_row < MAP_RANGE and new_col >= 0 and new_col < MAP_RANGE and not visited[new_row][new_col] and arr[new_row][new_col] >= 0:
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

                        if new_row >= 0 and new_row < MAP_RANGE and new_col >= 0 and new_col < MAP_RANGE and arr[new_row][new_col] > 0:
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

                        if new_row >= 0 and new_row < MAP_RANGE and new_col >= 0 and new_col < MAP_RANGE and arr[new_row][new_col] > 0:
                            neighbors += 1

                    if neighbors == 1:
                        key_rooms["boss"] = [row, col]

                elif arr[row][col] >= furthest_distance // 2 and arr[row][col] <= furthest_distance - 1:
                    neighbors = 0
                    for i in range(4):
                        new_row = row + d_row[i]
                        new_col = col + d_col[i]

                        if new_row >= 0 and new_row < MAP_RANGE and new_col >= 0 and new_col < MAP_RANGE and arr[new_row][new_col] > 0:
                            neighbors += 1

                    if neighbors == 1:
                        key_rooms["shop"] = [row, col]

        if key_rooms["start"] is None or key_rooms["shop"] is None or key_rooms["boss"] is None:
            return False, key_rooms

        return True, key_rooms