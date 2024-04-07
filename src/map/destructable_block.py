import pygame
from config import *
from .block import Block

class DestructableBlock(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image.fill(GREY)
        self.durability = 5

    def get_hit(self, dmg):
        self.durability -= dmg
        if self.durability <= 0:
            self.kill()
            self.game.map.get_current_room().remove_block(self)