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
        
        #self.groups = self.game.all_sprites, self.game.blocks
        self.groups = self.game.chest, self.game.collidables
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
        if not self.opened_once:
            itmes = []
            self.is_open = True
            self.image.fill(RED)
            self.opened_once = True

            self.drop_loot(itmes)

            return itmes



    def drop_loot(self, items_to_craft:list):
        if self.type == "small":
            #silver coin
            for _ in range(random.randint(5, 5)):
                items_to_craft.append(Lootable_item(self.game, self.rect.centerx, self.rect.centery))


        #rest to implement
        #elif self.type == "medium":
        #    self.contents["silver_coin"] = random.randint(3, 5)
        #    self.contents["golden_coin"] = random.randint(1, 2)
        #    self.contents["health_potion"] = random.randint(0, 1)

        #elif self.type == "large":
        #    self.contents["silver_coin"] = random.randint(5, 10)
        #    self.contents["golden_coin"] = random.randint(2, 5)
        #    self.contents["health_potion"] = 1


    def animate_opening(self):
        pass