import pygame

from items.item_types import ItemType

from ..lootable_item import LootableItem


class PickupBomb(LootableItem):
    def __init__(self, game, x, y, amount=1, drop_animation=True):
        super().__init__(game, x, y, drop_animation)

        self.image = game.image_loader.lootables["bomb"]

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.mask = pygame.mask.from_surface(self.image)
        self.amount = amount

    def picked_up(self):
        self.clean_up()
        self.kill()
        self.is_picked_up = True
        self.game.sound_manager.play_if_not_playing("lift")

        return ItemType.PICKUP_BOMB, self.amount
