import random
import pygame
from config import BASE_BULLET_FLY_TIME, DIAGONAL_MULTIPLIER, PLAYER_SHOOT_DIAGONAL
from entities.bullet import Bullet
from entities.laser import Laser
from utils.directions import Directions

class ShootingEnginge():
    key_to_direction = {
            pygame.K_LEFT: Directions.LEFT,
            pygame.K_RIGHT: Directions.RIGHT,
            pygame.K_UP: Directions.UP,
            pygame.K_DOWN: Directions.DOWN
        }
    
    def __init__(self, player, game):
        self.player = player
        self.game = game

        #SHOOTING
        self.shot_time_left = 0
        self.shot_try = False

        #SECOND SHOOT
        self.shoot_second_bullet = 0
        self.shoot_second_time = 0

    def shoot(self, keys, x_y_vel):
        self.shot_time_left -= 1
        self.shoot_second_bullet -= 1
        self.shot_try = False
        
        for key, direction in self.key_to_direction.items():
            if keys[key]:
                self.player.facing = direction
                self.shot_try = True
            
        if self.shot_try or self.shoot_second_bullet >= 0:
            if self.shot_time_left <= 0:
                self.shot_time_left = self.player.get_shooting_cooldown() 
                if self.player.eq.extra_stats["extra_shot_time"]:
                    self.shoot_second_bullet = self.player.eq.extra_stats["extra_shot_time"]
                self.shoot_one_bullet(x_y_vel)

            elif self.shoot_second_bullet == 0:
                self.shoot_one_bullet(x_y_vel)
                self.shot_time_left = self.player.get_shooting_cooldown()
            else:
                self.shot_try = False

    def shoot_one_bullet(self, x_y_vel):
        additional_v = 0
        if PLAYER_SHOOT_DIAGONAL:
            _, other_axis_index = self.player.facing.rotate_clockwise().get_axis_tuple()     
            if x_y_vel[other_axis_index]:
                additional_v = int(self.player.get_shot_speed() * x_y_vel[other_axis_index] * DIAGONAL_MULTIPLIER) 

        x, y = self.calculate_bullet_position()
        self.player.player_animation.reset_tear_shot_cd()
        """
        Bullet(self.game, x, y, self.player.facing, self.player.get_shot_speed(), True,
                (self.player.dmg+self.player.eq.stats["dmg"])*self.player.eq.extra_stats["dmg_multiplier"], 
                BASE_BULLET_FLY_TIME+self.player.eq.stats["bullet_fly_time"], additional_speed=additional_v)
        """
        Laser(self.game, x, y, self.player.facing, True, 1, 1)
        self.game.sound_manager.play(f"tear{random.randint(1, 2)}")
        
    def calculate_bullet_position(self):
        x, y = self.player.rect.centerx, self.player.rect.centery
        if self.player.facing == Directions.LEFT:
            x -= self.player.PLAYER_SIZE//2
        elif self.player.facing == Directions.RIGHT:
            x += self.player.PLAYER_SIZE//2
        elif self.player.facing == Directions.UP:
            y -= self.player.PLAYER_SIZE//2
        elif self.player.facing == Directions.DOWN:
            y += self.player.PLAYER_SIZE//2
        return x, y