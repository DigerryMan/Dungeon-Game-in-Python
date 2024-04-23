import pygame
from config import *
from ..lootable_item import LootableItem

class Health_potion(LootableItem):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)
        

    def picked_up(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        
        if hits:
            current_room = self.game.map.get_current_room()
            current_room.remove_item(self)
            self.kill()