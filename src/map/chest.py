import pygame
import random
from config import *
from .lootables.lootable_item import Lootable_item


class Chest(pygame.sprite.Sprite):
    type = ["small", "medium", "large"]

    def __init__(self, game, x, y, type):
        self.game = game
        self._layer = BLOCK_LAYER
        self.type = type
        self.is_open = False
        self.opened_once = False
        self.contents = {
            "silver_coin": [],
            "golden_coin": [],
            "health_potion": []
        }
        
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

        self.set_contents()

    def open(self):
        if not self.opened_once:
            #print("Chest opened")
            self.is_open = True
            self.image.fill(RED)
            self.opened_once = True

    def update(self, screen):
        if self.is_open:
            self.drop_loot(screen)
        
    
    def set_contents(self):
        if self.type == "small":
            self.contents["silver_coin"] = [Lootable_item(self.game, self.rect.centerx, self.rect.centery) for _ in range(random.randint(5, 5))]

        elif self.type == "medium":
            self.contents["silver_coin"] = random.randint(3, 5)
            self.contents["golden_coin"] = random.randint(1, 2)
            self.contents["health_potion"] = random.randint(0, 1)

        elif self.type == "large":
            self.contents["silver_coin"] = random.randint(5, 10)
            self.contents["golden_coin"] = random.randint(2, 5)
            self.contents["health_potion"] = 1

    def drop_loot(self, screen):
        for arr in self.contents.values():
            if arr:
                for item in arr:
                    item.drop(screen)


    def animate_opening(self):
        pass