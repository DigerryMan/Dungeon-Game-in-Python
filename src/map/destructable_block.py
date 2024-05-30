import random
import pygame
from .block import Block

class DestructableBlock(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = game.image_loader.blocks["vase" + str(random.randint(1, 4))].copy()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.durability = 3

    def get_hit(self):
        self.durability -= 1
        if self.durability <= 0:
            self.kill()
            self.game.map.get_current_room().remove_block(self)
            self.game.sound_manager.play("rockBreak")