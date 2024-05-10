import random
import pygame

from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from .block import Block

class TreasureBlock(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = game.image_loader.blocks["treasure_rock" + str(random.randint(1, 2))].copy()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_bombed(self):
        super().get_bombed()
        rand = random.random()
        room = self.game.map.get_current_room()
        if rand < 0.5:
            room.items.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery))
        elif rand < 0.8:
            room.items.append(GoldenCoin(self.game, self.rect.centerx, self.rect.centery))
        else:
            room.items.append(PickupHeart(self.game, self.rect.centerx, self.rect.centery))