import random

import pygame

from map.destructable_block import DestructableBlock


class Poop(DestructableBlock):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.type = random.randint(0, 4)
        self.image = game.image_loader.blocks[f"poop{self.type}_4"].copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.durability = 4

    def get_hit(self):
        self.durability -= 1
        if self.durability >= 0:
            self.update_image()

        if self.durability <= 0:
            self.game.sound_manager.play_if_not_playing("fart")

    def update_image(self):
        self.image = self.game.image_loader.blocks[
            f"poop{self.type}_{self.durability}"
        ].copy()
