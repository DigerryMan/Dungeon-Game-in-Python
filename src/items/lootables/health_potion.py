import pygame
from config import *
from items.item_types import ItemType
from ..lootable_item import LootableItem

class HealthPotion(LootableItem):
    def __init__(self, game, x, y, heal_value = 1):
        super().__init__(game, x, y)
        self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)
        self.heal_value = heal_value
        

    def picked_up(self):
        self.clean_up()
        self.kill()
        self.is_picked_up = True

        return ItemType.HEALTH_POTION, self.heal_value