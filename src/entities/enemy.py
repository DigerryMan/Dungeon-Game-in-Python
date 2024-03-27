import pygame
import random
from config import *
from entities.bullet import Bullet
from utils.directions import Directions

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x:int, y:int, check_block_colisions:bool=True, is_wandering:bool=True):
        #CHANGEABLE STATS
        self._health = 2
        self._damage = 1
        self._collision_damage = 1
        self._attack_speed = 800
        
        self._speed = 3
        self._projectal_speed = 10
        self._shot_cd = 2500

        self._wander_interval = [700,1700]
        self._idle_interval = [1200,2500]

        #POSITION
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.x_change = 0
        self.y_change = 0
        
        #SKINS
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.animation_loop = 1


        #HITBOX
        self.rect = self.image.get_rect()
        self.rect.x = x * self.width
        self.rect.y = y * self.height
        self._layer = self.rect.bottom
     
        #REST
        self._check_block_colisions = check_block_colisions
        self.facing = random.choice([Directions.LEFT, Directions.RIGHT])

        self._last_attack = pygame.time.get_ticks()
        self._last_shot = pygame.time.get_ticks()
        self._is_wandering = is_wandering
        self._wander_time = self.roll_interval(self._wander_interval)
        self._idle_time = self.roll_interval(self._idle_interval)
        self._is_idling = self._is_wandering
        self._last_idle = pygame.time.get_ticks()
        self._last_wander = pygame.time.get_ticks()

        self.game = game
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
   

    def update(self):
        self.move()
        self.collide_player()
        if not self._is_wandering:
            self.attack()

        self.rect.x += self.x_change
        if self._check_block_colisions:
            self.collide_blocks('x')

        self.rect.y += self.y_change
        if self._check_block_colisions:
            self.collide_blocks('y')
        
        self.correct_facing()
        self.correct_layer()
        self.animate()

        self.x_change = 0
        self.y_change = 0

    def move(self):
        if self._is_wandering:
            self.wander()
        else:
            self.chase_player() 
        
    def wander(self):
        if self._is_idling:
            self.idle()
        
        else:
            now = pygame.time.get_ticks()
            if now - self._last_idle > self._wander_time:
                self._last_wander = now
                self._is_idling = True
                self._wander_time = self.roll_interval(self._wander_interval)
            
            else:
                if self.facing == Directions.LEFT:
                    self.x_change = -self._speed//2
                elif self.facing == Directions.RIGHT:
                    self.x_change = self._speed//2
                elif self.facing == Directions.UP:
                    self.y_change = -self._speed//2
                elif self.facing == Directions.DOWN:
                    self.y_change = self._speed//2

    def idle(self):
        now = pygame.time.get_ticks()
        if now - self._last_wander > self._idle_time:
            self._last_idle = now
            self._is_idling = False
            self.roll_facing()
            self._idle_time = self.roll_interval(self._idle_interval)

    def chase_player(self):
        player_vector = pygame.math.Vector2(self.game.get_player_rect().center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

        distance = (player_vector - enemy_vector).magnitude()
        direction = None

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        
        velocity = direction * self._speed

        self.x_change = velocity.x
        self.y_change = velocity.y
        self._correct_rounding()
        self.correct_facing()

    def collide_player(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
        if hits:
            self.game.damage_player(self._collision_damage)
            self.game.playing = False
            self._is_wandering = False

    def attack(self):
        now = pygame.time.get_ticks()
        if now > self._last_shot + self._shot_cd:
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.PLAYER, self._projectal_speed, False)
            self._last_shot = now
            self.roll_next_shot_cd()

    def collide_blocks(self, orientation:str):
        hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if hits:
            if orientation == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

            if orientation == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def _correct_rounding(self):
        if self.x_change < 0:
            self.x_change = self.x_change - 1
        else:
            self.x_change = self.x_change + 1

        if self.y_change < 0:
            self.y_change = self.y_change - 1
        else:
            self.y_change = self.y_change + 1

    def roll_facing(self):
        rand = random.randint(1, 4)
        if rand == 1:
            self.facing = self.facing.rotate_clockwise()

        elif rand == 2:
            self.facing = self.facing.rotate_counter_clockwise()
           
        elif rand == 3:
            self.facing = self.facing.reverse()

    def correct_facing(self):
        y_abs = abs(self.y_change)
        x_abs = abs(self.x_change)

        if(x_abs >= y_abs):
            if self.x_change < 0:
                self.facing = Directions.LEFT
            elif self.x_change > 0:
                self.facing = Directions.RIGHT
        else:
            if self.y_change < 0:
                self.facing = Directions.UP
            elif self.y_change > 0:
                self.facing = Directions.DOWN 

    def get_hit(self, dmg:int):
        self._health -= dmg
        self._is_wandering = False
        self.check_if_dead()
    
    def check_if_dead(self):
        if self._health <= 0:
            self.kill()

    def roll_interval(self, interval):
        return random.randint(interval[0], interval[1])

    def roll_next_shot_cd(self):
        self._shot_cd = random.randint(1500, 3000)

    def animate(self):
        pass
            
    def correct_layer(self):
        self._layer = self.rect.bottom