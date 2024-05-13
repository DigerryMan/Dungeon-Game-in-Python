import pygame
from items.item_types import ItemType
from items.lootable_item import LootableItem
from items.stat_items.categories import Categories

class Item(LootableItem):
    def __init__(self, game, x, y, category, drop_animation = True):
        super().__init__(game, x, y, drop_animation)
        
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
        self.item = self.game.items_list.get_random_item(category)
        #self.item = self.game.items_list.legendaries["friendly_ghost"]

    def picked_up(self):
        if not self.game.space_pressed:
            return None, None
        
        self.clean_up()
        self.kill()
        self.is_picked_up = True

        if self.item["category"] == Categories.VERY_COMMON:
            return ItemType.PILL, self.item
        
        return ItemType.ITEM, self.item