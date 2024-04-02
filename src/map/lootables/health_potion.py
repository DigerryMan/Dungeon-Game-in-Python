import pygame
from config import *
from .lootable_item import Lootable_item

class Health_potion(Lootable_item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image.fill(RED)
        

    def picked_up(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        
        if hits:
            current_room = self.game.map.get_current_room()
            current_room.remove_item(self)
            print("Health potion picked up")
            self.kill()