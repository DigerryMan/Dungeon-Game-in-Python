import random
import pygame
from config import *
from entities.enemy import Enemy
from utils.directions import Directions

class Maggot(Enemy):
    def __init__(self, game, x, y, moving_clockwise=random.choice([True, False])):
        super().__init__(game, x, y, False)
        #CHANGEABLE STATS
        self._health = 4
        self._speed = 3 * game.settings.WINDOW_SIZE_SPEED_FACTOR
        self._random_dir_change_cd = int(2 * FPS)
        
        #SKIN
        self.x_frame = 0
        self.y_frame = 0
        self.reversed_frame = False
        
        self.next_frame_ticks_cd = 5
        self.time = self.next_frame_ticks_cd

        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = game.image_loader.get_image("maggot")
        self.frame = self.img.subsurface(pygame.Rect(self.x_frame, 0, 32, 32))
        self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
        self.head_frame = None
        self.body_frame = None

        #REST
        self.moving_clockwise = moving_clockwise
        self._change_of_direction_time_left = self._random_dir_change_cd
                
    def move(self):
        self.wall_collision()
        self.random_change_of_direction()
        if self.facing == Directions.LEFT:
            self.x_change -= self._speed

        if self.facing == Directions.RIGHT:
            self.x_change += self._speed
        
        if self.facing == Directions.UP:
            self.y_change -= self._speed

        if self.facing == Directions.DOWN:
            self.y_change += self._speed
        
    def attack(self):
        pass

    def wall_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.collidables, False)

        if hits:
            if self.facing == Directions.LEFT:
                self.rect.x = hits[0].rect.right 

            elif self.facing == Directions.RIGHT:
                self.rect.x = hits[0].rect.left - self.game.settings.MOB_SIZE

            elif self.facing == Directions.UP:
                self.rect.y = hits[0].rect.bottom

            elif self.facing == Directions.DOWN:
                self.rect.y = hits[0].rect.top - self.game.settings.MOB_SIZE

            self.rotate_facing()
            
    def random_change_of_direction(self):
        self._change_of_direction_time_left -= 1
        if self._change_of_direction_time_left <= 0:
            self.roll_rotation_cd(int(0.4 * FPS), int(2.2 * FPS))
            self._change_of_direction_time_left = self._random_dir_change_cd
            
            self.rotate_facing()

    def rotate_facing(self):
        if self.moving_clockwise:
            self.facing = self.facing.rotate_clockwise()
        else:
            self.facing = self.facing.rotate_counter_clockwise()

        
    def roll_rotation_cd(self, mini:int, maxi:int):
        self._random_dir_change_cd = random.randint(mini, maxi)

    def next_frame(self):
        self.x_frame = (self.x_frame + 1) % 4
        self.set_y_frame() 
        self.set_head_frame()
        self.body_frame = self.img.subsurface(pygame.Rect(self.x_frame * 32, self.y_frame * 32, 32, 32))
        self.body_frame = pygame.transform.scale(self.body_frame, (self.MOB_SIZE, self.MOB_SIZE))
        self.frame = (pygame.Surface((self.MOB_SIZE, self.MOB_SIZE), pygame.SRCALPHA))

        self.frame.blit(self.body_frame, (0, 0))
        if self.facing == Directions.DOWN:
            self.frame.blit(self.head_frame, ((self.MOB_SIZE - self.head_frame.get_width())//2, (self.MOB_SIZE)*0.3))
            pass
        elif self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            self.frame.blit(self.head_frame, (self.MOB_SIZE*0.65 - self.head_frame.get_height()//2, (self.MOB_SIZE-self.head_frame.get_height())//2 + 2))
            pass

        if self.reversed_frame:
            self.frame = pygame.transform.flip(self.frame, True, False)

        self.remove_transparency_from_frame()
       
    def set_y_frame(self):
        self.reversed_frame = False
        if self.facing == Directions.LEFT:
            self.y_frame = 0
            self.reversed_frame = True
        elif self.facing == Directions.RIGHT:
            self.y_frame = 0
        elif self.facing == Directions.UP:
            self.y_frame = 1
        elif self.facing == Directions.DOWN:
            self.y_frame = 2
    
    def set_head_frame(self):
        x = 0
        if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
            x = 1
        if self.facing == Directions.UP:
            x = 2
        
        self.head_frame = self.img.subsurface(pygame.Rect(x * 32, 3 * 32, 32, 32))
        self.head_frame = pygame.transform.scale(self.head_frame, (self.MOB_SIZE*0.75, self.MOB_SIZE*0.75))

    def remove_transparency_from_frame(self):
        bounding_rect = self.frame.get_bounding_rect() 
        self.image = self.frame.subsurface(bounding_rect)
        self.rect.width, self.rect.height = self.image.get_rect().width, self.image.get_rect().height

    def animate(self):
        self.time -= 1
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd
            self.next_frame()
    