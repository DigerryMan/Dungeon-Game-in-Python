import pygame
from config import *
from ..lootable_item import LootableItem

class SilverCoin(LootableItem):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image.fill(SILVER)
        self.mask = pygame.mask.from_surface(self.image)

    def picked_up(self):
        self.clean_up()
        return 1