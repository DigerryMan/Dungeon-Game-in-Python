import pygame
import random
from config import *

class LootableItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y, drop_animtion = True):
        self.game = game
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self._layer = self.rect.centery

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.is_picked_up = False

        if drop_animtion:
            TS = game.settings.TILE_SIZE
            self.drop_animation_time = 40
            self.horizontal_velocity = random.uniform(-3, 3) * game.settings.SCALE

            x = self.horizontal_velocity * self.drop_animation_time
            y = -(((5/4) * TS**2 - x**2)**0.5)

            #final_x = x + self.x
            final_y = y + self.y + TS//4

            self.acceleration = 0.5 * game.settings.SCALE
            self.vertical_velocity = -((self.y - final_y - (self.acceleration * self.drop_animation_time**2)/2) / self.drop_animation_time)
            self.vertical_velocity *= random.uniform(0.9, 1.1)

        else:
            self.drop_animation_time = 0


    def update(self):
        self.drop_animation()
        self._layer = self.rect.centery

    def drop_animation(self):
        if self.drop_animation_time > 0:
            self.vertical_velocity -= self.acceleration
            self.y -= self.vertical_velocity
            self.x += self.horizontal_velocity
            self.rect.x = round(self.x)
            self.rect.y = round(self.y)
            self.drop_animation_time -= 1

    def picked_up(self):
        pass
    
    def clean_up(self):
        current_room = self.game.map.get_current_room()
        current_room.remove_item(self)