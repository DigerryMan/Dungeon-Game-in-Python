import pygame
from config import *
from entities.player.equipment import Equipment
from ..bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #MAIN
        self.game = game
        self.max_health = BASE_HEALTH
        self.health = BASE_HEALTH
        self.__speed = BASE_SPEED
        self.coins = 100

        #SIZE
        self.width = game.settings.PLAYER_SIZE
        self.height = game.settings.PLAYER_SIZE

        #SKIN
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        
        #HITBOX / POSITION
        self.rect = self.image.get_rect()
        self.rect.x = x * self.width
        self.rect.y = y * self.height
        
        #EQ
        self.eq = Equipment(self)
        self.eq_opened = False
        
        #REST
        self._layer = self.rect.bottom
        self.__immortality_time_left = 0
        self.__shot_time_left = 0
        self.facing = Directions.DOWN
        self.x_change = 0
        self.y_change = 0
        
        self.groups = self.game.all_sprites, self.game.player_sprite, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)
    
    def update(self):
        self._user_input()
        self._correct_diagonal_movement()

        self.rect.x += self.x_change
        self._collide_blocks('x')
        self.rect.y += self.y_change
        self._collide_blocks('y')

        self._check_items_pick_up()
        
        self._layer = self.rect.bottom
        self.animate()

        self.__immortality_time_left -= 1
        self.x_change = 0
        self.y_change = 0

    def _user_input(self):
        keys = pygame.key.get_pressed()
        x_y_vel = [0,0]
        self._move(keys, x_y_vel)
        self._shoot(keys, x_y_vel)

    def _move(self, keys, x_y_vel):
        if keys[pygame.K_a]:
            self.x_change -= self.__speed
            self.facing = Directions.LEFT
            x_y_vel[0] -= 1
        
        if keys[pygame.K_d]:
            self.x_change += self.__speed
            self.facing = Directions.RIGHT
            x_y_vel[0] += 1

        if keys[pygame.K_w]: 
            self.y_change -= self.__speed
            self.facing = Directions.UP
            x_y_vel[1] -= 1

        if keys[pygame.K_s]:
            self.y_change += self.__speed
            self.facing = Directions.DOWN
            x_y_vel[1] += 1

    def _shoot(self, keys, x_y_vel):
        self.__shot_time_left -= 1
        if self.__shot_time_left <= 0:
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
                self.__shot_time_left = self.get_shooting_cooldown()
                additional_v = 0
                
                if PLAYER_SHOOT_DIAGONAL:
                    _, other_axis_index = direction.rotate_clockwise().get_axis_tuple()     
                    if x_y_vel[other_axis_index]:
                        additional_v = int(self.get_shot_speed() * x_y_vel[other_axis_index] * DIAGONAL_MULTIPLIER) 

                Bullet(self.game, self.rect.centerx, self.rect.centery, direction, self.get_shot_speed(), True,
                        BASE_DMG+self.eq.stats["dmg"], BASE_BULLET_FLY_TIME+self.eq.stats["bullet_fly_time"],
                       additional_speed=additional_v)

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

    def _check_items_pick_up(self):
        hits = pygame.sprite.spritecollide(self, self.game.items, False)
        for item in hits:
            item_info = item.picked_up()
            
            if isinstance(item_info, int): #coins
                self.coins += item_info
            else:                          #items
                self.eq.add_item(item_info)

    def animate(self):
        pass

    def set_rect_position(self, x_rect, y_rect):
        self.rect.x = x_rect
        self.rect.y = y_rect

    def get_hit(self, dmg:int):
        if self.__immortality_time_left <= 0:
            self.health -= dmg * (1 - self.eq.stats["dmg_reduction"])
            self.__immortality_time_left = self.get_immortality_time()
            print(self.health)
            self._check_is_dead()

    def _check_is_dead(self):
        if self.health <= 0 and not GOD_MODE:
            self.game.game_over()
    
    def get_center_position(self):
        return self.rect.centerx, self.rect.centery
    
    def heal(self, amount:int):
        self.health = min(self.max_health, self.health + amount)

    def update_player_stats(self):
        self.max_health = BASE_HEALTH + self.eq.stats["health"]
        self.__speed = BASE_SPEED + self.eq.stats["speed"]
    
    def get_shooting_cooldown(self):
        return int((BASE_SHOOTING_COOLDOWN - self.eq.stats["shooting_cd_decrease"]) * FPS)

    def get_immortality_time(self):
        return int((BASE_IMMORTALITY_AFTER_HIT + self.eq.stats["extra_immortality"]) * FPS)

    def get_shot_speed(self):
        return BASE_SHOT_SPEED + self.eq.stats["shot_speed"]
    
    def get_luck(self):
        return BASE_LUCK + self.eq.stats["luck"]