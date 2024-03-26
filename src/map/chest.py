import pygame
import random
from config import *
from .lootables import *


class Chest(pygame.sprite.Sprite):
    type = ["small", "medium", "large"]

    def __init__(self, game, x, y, type):
        self.game = game
        self._layer = BLOCK_LAYER
        self.type = type
        self.is_open = False
        self.opened_once = False
        self.contents = {
            "silver_coin": 0,
            "golden_coin": 0,
            "health_potion": 0
        }
        self.set_contents()
        #self.groups = self.game.all_sprites, self.game.blocks
        self.groups = self.game.chests, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(ORANGE)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def open(self):
        self.is_open = True
        self.image.fill(RED)
        if not self.opened_once:
            self.drop_loot()
            self.opened_once = True
        
    
    def set_contents(self):
        if self.type == "small":
            self.contents["silver_coin"] = random.randint(1, 3)

        elif self.type == "medium":
            self.contents["silver_coin"] = random.randint(3, 5)
            self.contents["golden_coin"] = random.randint(1, 2)
            self.contents["health_potion"] = random.randint(0, 1)

        elif self.type == "large":
            self.contents["silver_coin"] = random.randint(5, 10)
            self.contents["golden_coin"] = random.randint(2, 5)
            self.contents["health_potion"] = 1

    def drop_loot(self):
        self.animate_opening()
        pass

    def animate_opening(self):
        pass