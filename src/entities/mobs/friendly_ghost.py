import random
from config import LIGHT_GREEN
from entities.bullet import Bullet
from entities.mobs.ghost import Ghost
from utils.directions import Directions
import pygame

class FriendlyGhost(Ghost):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._health = 3333
        self.damage = 1
        self.speed = 1
        self._projectal_speed = 10

        #SKINS
        self.image.fill(LIGHT_GREEN)
        
        self.groups = game.all_sprites, game.entities
        self.remove(game.enemies)

    def attack(self):
        self._shot_time_left -= 1
        if self._shot_time_left <= 0 and self.game.enemies:
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.ENEMY, 
                   self._projectal_speed, True, self._damage, self._bullet_decay_sec)
            self.roll_next_shot_cd()
            self._shot_time_left = self._shot_cd
    
    def move_because_of_player(self, chase:bool=True):
        player_horizontal_facing = self.game.player.last_horizontall_facing
        player_rect = self.game.get_player_rect()
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = None

        if player_horizontal_facing == Directions.LEFT:
            player_vector = pygame.math.Vector2(player_rect.left, player_rect.top)
        else:
            player_vector = pygame.math.Vector2(player_rect.right, player_rect.top)
     
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 3:
            direction = None

            if distance > 0:
                direction = (player_vector - enemy_vector).normalize()
            else:
                direction = pygame.math.Vector2()
            
            speed = self._speed
            if not chase:
                direction.rotate_ip(180)
                speed = self._speed * self._chase_speed_debuff

            velocity = direction * speed

            self.x_change = velocity.x
            self.y_change = velocity.y
            self._correct_rounding()
            self.correct_facing()

    def collide_player(self):
        pass