import pygame
import random
from config import *
from items.lootables.silver_coin import SilverCoin
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.stat_items.categories import Categories
from items.stat_items.item import Item

class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self._layer = BLOCK_LAYER
        self.type = type
        self.is_open = False
        self.opened_once = False

        self.groups = self.game.all_sprites, self.game.chest, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * game.settings.TILE_SIZE
        self.y = y * game.settings.TILE_SIZE
        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE

        self.images = [game.image_loader.chests[f"{self.type}_chest{i}"].copy() for i in range(8)]
        self.image = self.images[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.mask = pygame.mask.from_surface(self.image)

        self.current_frame = 0
        self.time_per_frame = 4
        self.timer = self.time_per_frame * (len(self.images) - 1)


    def open(self):
        if not self.opened_once:
            items = []
            self.is_open = True
            self.opened_once = True

            self.drop_loot(items)

            return items

    def update(self):
        if self.is_open and self.timer > 0:
            self.timer -= 1 
            if self.timer % self.time_per_frame == 0:
                self.next_frame()

    def next_frame(self):
        self.current_frame += 1
        self.image = self.images[self.current_frame]

    def drop_loot(self, items_to_craft:list):
        if self.type == "small":
            for _ in range(random.randint(2, 4)):
                items_to_craft.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery))

            items_to_craft.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.LEGENDARY))

        elif self.type == "medium":
            for _ in range(random.randint(3, 5)):
                items_to_craft.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery))

            for _ in range(random.randint(1, 2)):
                items_to_craft.append(GoldenCoin(self.game, self.rect.centerx, self.rect.centery))

            for _ in range(random.randint(0, 1)):
                items_to_craft.append(PickupHeart(self.game, self.rect.centerx, self.rect.centery))

        elif self.type == "large":
            for _ in range(random.randint(5, 10)):
                items_to_craft.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery))

            for _ in range(random.randint(2, 5)):
                items_to_craft.append(GoldenCoin(self.game, self.rect.centerx, self.rect.centery))

            for _ in range(1):
               items_to_craft.append(PickupHeart(self.game, self.rect.centerx, self.rect.centery))

            items_to_craft.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.LEGENDARY))