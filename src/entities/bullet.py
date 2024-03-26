import pygame

from config import *
from utils.directions import Directions

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:Directions, speed=20, is_friendly=True, dmg=1):
        #MAIN
        self.dmg = dmg
        self.direction = direction
        self.is_friendly = is_friendly
        self.speed = speed

        #POSITION / SIZE
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT

        #SKIN
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BROWN)

        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #REST
        self.x_change = 0
        self.y_change = 0
        
        self.game = game
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        if self.direction == Directions.PLAYER: #for shot to player position
            self.speed_x = 0
            self.speed_y = 0
            self._calculate_speed_to_player()

    def update(self):
        self.move()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        self._collide()
        self._layer = self.rect.bottom

        self.x_change = 0
        self.y_change = 0

    def move(self):
        if(self.direction == Directions.UP):
            self.y_change -= self.speed

        elif(self.direction == Directions.DOWN):
            self.y_change += self.speed

        elif(self.direction == Directions.LEFT):
            self.x_change -= self.speed

        elif(self.direction == Directions.RIGHT):
            self.x_change += self.speed
        
        elif(self.direction == Directions.PLAYER):
            self.x_change += self.speed_x
            self.y_change += self.speed_y

    def _calculate_speed_to_player(self):
        player_vector = pygame.math.Vector2(self.game.get_player_rect().center)
        bullet_vector = pygame.math.Vector2(self.rect.center)
        distance = (player_vector - bullet_vector).magnitude()
        direction = None
        
        if distance > 0:
            direction = (player_vector - bullet_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        
        velocity = direction * self.speed
        self.speed_x = int(velocity.x)
        self.speed_y = int(velocity.y)

    def _collide(self):
        if self.is_friendly:       
            mob_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if mob_hits and mob_hits[0] not in self.game.not_voulnerable:
                mob_hits[0].get_hit(self.dmg)
                self.kill()
            
        else:
            player_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if player_hits:
                player_hits[0].get_hit(self.dmg)
                self.kill()
            
        block_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if block_hits:
            self.kill()


            