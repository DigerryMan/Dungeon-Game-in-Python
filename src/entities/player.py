import pygame
from config import *
from .bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #MAIN
        self.game = game
        self.__health = 3
        self.__dmg = 1
        self.speed = 9
        self.__immortality_after_hit = 1000
        self.__shooting_cooldown = 500
        self.__shot_speed = 20

        #SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        #SKIN
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        
        #HITBOX / POSITION
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        #REST
        self._layer = self.rect.bottom
        self.__last_hit = pygame.time.get_ticks()
        self.__last_shot = pygame.time.get_ticks()
        self.facing = Directions.DOWN
        self.x_change = 0
        self.y_change = 0

        self.groups = self.game.all_sprites, self.game.player_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
    
    def update(self):
        self._user_input()
        self._correct_diagonal_movement()

        self.rect.x += self.x_change
        self._collide_blocks('x')
        self.rect.y += self.y_change
        self._collide_blocks('y')

        self._layer = self.rect.bottom
        self.animate()

        self.x_change = 0
        self.y_change = 0

    def _user_input(self):
        keys = pygame.key.get_pressed()
        x_y_vel = [0,0]
        self._move(keys, x_y_vel)
        self._shoot(keys, x_y_vel)

    def _move(self, keys, x_y_vel):
        if keys[pygame.K_a]:
            self.x_change -= self.speed
            self.facing = Directions.LEFT
            x_y_vel[0] -= 1
        
        if keys[pygame.K_d]:
            self.x_change += self.speed
            self.facing = Directions.RIGHT
            x_y_vel[0] += 1

        if keys[pygame.K_w]: 
            self.y_change -= self.speed
            self.facing = Directions.UP
            x_y_vel[1] -= 1

        if keys[pygame.K_s]:
            self.y_change += self.speed
            self.facing = Directions.DOWN
            x_y_vel[1] += 1

    def _shoot(self, keys, x_y_vel):
        now = pygame.time.get_ticks()
        if now - self.__last_shot > self.__shooting_cooldown:
            shot = False
            direction:Directions = None
            if keys[pygame.K_LEFT]:
                direction = Directions.LEFT
                shot = True

            if keys[pygame.K_RIGHT]:
                direction = Directions.RIGHT
                shot = True

            if keys[pygame.K_UP]:
                direction = Directions.UP
                shot = True

            if keys[pygame.K_DOWN]:
                direction = Directions.DOWN
                shot = True
            
            if shot:
                self.__last_shot = now
                additional_v = 0
                
                if PLAYER_SHOOT_DIAGONAL:
                    other_axis, other_axis_index = direction.rotate_clockwise().get_axis_tuple()     
                    if x_y_vel[other_axis_index]:
                        additional_v = int(self.__shot_speed * x_y_vel[other_axis_index] * DIAGONAL_MULTIPLIER) 

                Bullet(self.game, self.rect.centerx, self.rect.centery, direction, 
                       dmg=self.__dmg, additional_speed=additional_v)

            

    def _correct_diagonal_movement(self):
        if(self.x_change and self.y_change):
            self.x_change //= 1.41
            self.y_change //= 1.41
            if self.x_change < 0:
                self.x_change += 1
            if self.y_change < 0:
                self.y_change += 1
                
    def _collide_blocks(self, direction:str):
        hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if hits:
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

            if direction == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        pass

    def set_rect_position(self, x_rect, y_rect):
        self.rect.x = x_rect
        self.rect.y = y_rect

    def get_hit(self, dmg:int):
        now = pygame.time.get_ticks()
        if now - self.__last_hit > self.__immortality_after_hit:
            self.__health -= dmg
            self.__last_hit = now
            
            self._check_is_dead()
            print(self.__health)

    def _check_is_dead(self):
        if self.__health <= 0 and not GOD_MODE:
            self.game.game_over()
            print("KONIEC GRY!")
    