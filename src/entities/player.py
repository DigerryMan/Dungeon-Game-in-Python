import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name="Player1"):
        self.__health = 3
        self.__movement_speed = 100
        self.__name = name
        self._layer = PLAYER_LAYER
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.vel = 10
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.facing = 'down'

        self.game = game
        self.groups = self.game.all_sprites

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        pygame.sprite.Sprite.__init__(self, self.groups)
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.vel
            self.facing = 'left'
        
        if keys[pygame.K_d]:
            self.x += self.vel
            self.facing = 'right'


        if keys[pygame.K_w]: 
            self.y -= self.vel
            self.facing = 'up'


        if keys[pygame.K_s]:
            self.y += self.vel
            self.facing = 'down'

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.move()