import pygame
from config import *
from entities.enemy import Enemy

class Fly(Enemy):
    is_group_attacked = False
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, check_block_colisions=True, 
                         is_wandering=True, bullet_decay_sec=2.0)
        #CHANGEABLE STATS
        self._health = 4
        self._speed = 1 * game.settings.SCALE
        self._projectal_speed = 6
        self._shot_cd = int(2.4 * FPS)

        #SKIN
        self.x_frame = 0
        self.y_frame = 0

        self.next_frame_ticks_cd = 3
        self.time = self.next_frame_ticks_cd
        self.next_frame_time = 3
        self.dead_animation_time = 10 * self.next_frame_time
        self.dead_animation_time_left = self.dead_animation_time
        

        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = game.image_loader.get_image("fly")
        self.frame = self.img.subsurface(pygame.Rect(self.x_frame, 0, 32, 32))
        self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
        self.image = self.frame

        self.mask = pygame.mask.from_surface(self.image)

    def animate(self):
        if not self._is_dead:
            self.time -= 1
            if self.time < 0:
                self.x_frame += 1
                self.x_frame %= 2
    
                self.frame = self.img.subsurface(pygame.Rect(self.x_frame * 32, self.y_frame * 32, 32, 32))
                self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
                self.image = self.frame

                self.time = self.next_frame_ticks_cd
        else:
            self.start_dying()

    def start_dying(self):
        self._is_dead = True
        if self.dead_animation_time_left == self.dead_animation_time:
            self.x_frame = 0
            self.y_frame = 1
            self.frame = self.img.subsurface(pygame.Rect(self.x_frame * 64, self.y_frame * 64, 64, 64))
            self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
            self.image = self.frame
        
        self.dead_animation_time_left -= 1
        if self.dead_animation_time_left < 0:
            self.kill()
        elif self.dead_animation_time_left % self.next_frame_time == 0:
            self.next_frame()

    def next_frame(self):
        self.x_frame += 1
        if self.x_frame % 4 == 0:
            self.x_frame = 0
            self.y_frame += 1

        self.frame = self.img.subsurface(pygame.Rect(self.x_frame * 64, self.y_frame * 64, 64, 64))
        self.frame = pygame.transform.scale(self.frame, (self.MOB_SIZE, self.MOB_SIZE))
        self.image = self.frame

    #Actually running away from the player
    def move_because_of_player(self, chase:bool=False):
        super().move_because_of_player(chase)
    
    @staticmethod
    def check_group_attacked():
        return Fly.is_group_attacked

    @staticmethod
    def group_attacked():
        Fly.is_group_attacked = True