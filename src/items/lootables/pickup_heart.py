import pygame

from items.item_types import ItemType

from ..lootable_item import LootableItem


class PickupHeart(LootableItem):
    def __init__(self, game, x, y, heal_value=1, drop_animation=True):
        super().__init__(game, x, y, drop_animation)
        if heal_value == 1:
            self.image = game.image_loader.lootables["full_heart"]

        else:
            self.image = game.image_loader.lootables["half_heart"]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.mask = pygame.mask.from_surface(self.image)
        self.heal_value = heal_value

    def picked_up(self):
        self.clean_up()
        self.kill()
        self.is_picked_up = True

        return ItemType.PICKUP_HEART, self.heal_value
