import pygame

from config import *
from utils.directions import Directions

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:Directions, speed=20, is_friendly=True, 
                 dmg=1, time_decay_in_seconds:float=0, additional_speed=0):
        #MAIN
        self.dmg = dmg
        self.direction = direction
        self.is_friendly = is_friendly
        self.speed = speed
        self.additional_speed = additional_speed
        self.time_decay = int(time_decay_in_seconds * FPS)
        self.time_left = self.time_decay

        #SIZE
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT

        #SKIN
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BROWN)

        #HITBOX / POSITION
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #REST
        self.x_change = 0
        self.y_change = 0

        self.game = game
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        if self.direction == Directions.PLAYER: 
            self._calculate_speed_to_player()
        else:
            self.calculate_speed()

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        self._collide()
        if self.time_decay:
            self.decay()
        self._layer = self.rect.bottom

    def calculate_speed(self):
        if(self.direction == Directions.UP):
            self.y_change = -self.speed

        elif(self.direction == Directions.DOWN):
            self.y_change = self.speed

        elif(self.direction == Directions.LEFT):
            self.x_change = -self.speed

        elif(self.direction == Directions.RIGHT):
            self.x_change = self.speed
        
        self.calculate_angled_speed()
        

    def calculate_angled_speed(self):
        axis, _ = self.direction.get_axis_tuple()
        if axis == 'x':
            self.y_change = self.additional_speed 
        elif axis == 'y':
            self.x_change = self.additional_speed
            
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
        self.x_change = int(velocity.x)
        self.y_change = int(velocity.y)

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
        door_hits = pygame.sprite.spritecollide(self, self.game.doors, False)
        if block_hits or door_hits:
            self.kill()

    def decay(self):
        self.time_left -= 1
        if self.time_left <= 0:
            self.kill()
            