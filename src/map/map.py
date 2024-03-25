from config import *
from .room_types import rooms
from .room import Room
from entities.player import *

class Map():
    def __init__(self, game, player:Player):
        self.room_map = [[None for _ in range(6)] for _ in range(6)]
        self.game = game
        self.player = player
        self._generate_rooms()

    def _generate_rooms(self):
        #tu na sztywno poki co
        room_type = 0

        self.room_map[0][0] = Room(room_type, self.player)

    def draw_room(self):
        room = self.room_map[0][0]
        room.draw_room(self.game)