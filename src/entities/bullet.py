import pygame

from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:str, is_friendly=True, dmg=1):
        self.dmg = dmg
        self.is_friendly = is_friendly
        self.width = 10
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.speed = 30
        self.direction = direction

        self.game = game
        self.groups = self.game.all_sprites, self.game.attacks

        pygame.sprite.Sprite.__init__(self, self.groups)

    def move(self):
        if(self.direction == "up"):
            self.y_change -= self.speed

        elif(self.direction == "down"):
            self.y_change += self.speed

        elif(self.direction == "left"):
            self.x_change -= self.speed

        elif(self.direction == "right"):
            self.x_change += self.speed
        pass

    def update(self):
        self.move()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        self._collide()

        self._layer = self.rect.bottom

        self.x_change = 0
        self.y_change = 0

    def _collide(self):
        if self.is_friendly:       
            mob_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if mob_hits:
                mob_hits[0].get_hit(self.dmg)
                self.kill()
            
        else:
            player_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if player_hits:
                player_hits[0].get_hit(self.dmg)
                self.kill()
            
        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        door_hits = pygame.sprite.spritecollide(self, self.game.doors, False)
        if block_hits or door_hits:
            self.kill()


            