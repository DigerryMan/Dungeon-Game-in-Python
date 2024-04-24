import pygame
from items.lootable_item import LootableItem
from items.stat_items.items_list import ItemsList

class Item(LootableItem):
    def __init__(self, game, x, y, category):
        super().__init__(game, x, y)
        
        self.item = None

        self.roll_item(category)

        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE
        
        self.image = self.item["image"]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.mask = pygame.mask.from_surface(self.image)
        

    def roll_item(self, category):
        #self.item = self.game.items_list.get_random_item(category)
        self.item = self.game.items_list.epics["glass_cannon"]

    def picked_up(self):
        self.clean_up()
        return self.item