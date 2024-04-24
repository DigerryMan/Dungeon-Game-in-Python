import pygame
import random
from config import *

class LootableItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y, drop_animtion = True):
        self.game = game
        self._layer = 0
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.horizontal_velocity = random.uniform(-3, 3) * game.settings.SCALE
        self.vertical_velocity = (10 - abs(self.horizontal_velocity)) * game.settings.SCALE
        self.acceleration = (0.6 - abs(self.horizontal_velocity) / 12) * game.settings.SCALE

        if drop_animtion:
            self.drop_animation_time = 40

        else:
            self.drop_animation_time = 0

        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self):
        self.drop_animation()

    def drop_animation(self):
        if self.drop_animation_time > 0:
            self.vertical_velocity -= self.acceleration
            self.y -= self.vertical_velocity
            self.x += self.horizontal_velocity
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            self.drop_animation_time -= 1

    def picked_up(self):
        self.clean_up()
        return None
    
    def clean_up(self):
        current_room = self.game.map.get_current_room()
        current_room.remove_item(self)