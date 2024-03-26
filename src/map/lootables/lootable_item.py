import pygame
import random
from config import *

class Lootable_item(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = 0
        #self.groups = self.game.all_sprites, self.game.blocks
        self.groups = self.game.blocks, self.game.collidables
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.acceleration = 1
        self.vertical_travel_time = 0
        self.vertical_velocity = 10
        self.horizontal_velocity = random.randint(-3, 3)

        self.x = x
        self.y = y
        self.width = TILE_SIZE // 20
        self.height = TILE_SIZE // 20

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def drop(self, screen):
        screen.blit(self.image, self.rect)
        if self.vertical_travel_time < 22:
            self.vertical_velocity -= self.acceleration
            self.rect.y -= self.vertical_velocity
            self.rect.x += self.horizontal_velocity
            self.vertical_travel_time += 1