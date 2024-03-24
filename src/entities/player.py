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

        self.x_change = 0
        self.y_change = 0

        self.game = game
        self.groups = self.game.all_sprites

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        pygame.sprite.Sprite.__init__(self, self.groups)
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x_change -= self.vel
            self.facing = 'left'
        
        if keys[pygame.K_d]:
            self.x_change += self.vel
            self.facing = 'right'


        if keys[pygame.K_w]: 
            self.y_change -= self.vel
            self.facing = 'up'


        if keys[pygame.K_s]:
            self.y_change += self.vel
            self.facing = 'down'



    def update(self):
        self.move()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0
    
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom