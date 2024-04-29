import random
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
        self.curr_frame = 0
        self.next_frame_ticks_cd = 3
        self.time = self.next_frame_ticks_cd
        self.next_frame_time = 3
        self.dead_animation_time = 10 * self.next_frame_time
        self.dead_animation_time_left = self.dead_animation_time
        
        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = game.image_loader.get_image("fly")
        
        self.images = []
        self.death_images = []
        self.prepare_images()

        self.frame = None
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        Fly.init_group_not_attacked()

    def prepare_images(self):
        multi = random.randint(0, 2)
        for x in range(multi, 2 + multi):
            self.images.append(self.img.subsurface(pygame.Rect(x * self.MOB_SIZE, 0, self.MOB_SIZE, self.MOB_SIZE)))       

        death_mob_size = self.MOB_SIZE * 2
        for y in range(1, 4):
            for x in range(4):
                self.death_images.append(self.img.subsurface(pygame.Rect(x * death_mob_size, y * death_mob_size, death_mob_size, death_mob_size)))       

    def collide_blocks(self, orientation:str):
        rect_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if rect_hits:
            if orientation == 'x':
                self.rect.x -= self.x_change

            if orientation == 'y':
                self.rect.y -= self.y_change

    def animate(self):
        if not self._is_dead:
            self.time -= 1
            if self.time < 0:
                self.curr_frame = (self.curr_frame + 1) % 2
                self.image = self.images[self.curr_frame]
                self.time = self.next_frame_ticks_cd
        else:
            self.start_dying()

    def start_dying(self):
        self._is_dead = True
        if self.dead_animation_time_left == self.dead_animation_time:
            self.curr_frame = 0
            self.image = pygame.transform.scale(self.death_images[self.curr_frame], (self.MOB_SIZE, self.MOB_SIZE))
        
        self.dead_animation_time_left -= 1
        if self.dead_animation_time_left < 0:
            self.kill()
            self.drop_lootable()
        elif self.dead_animation_time_left % self.next_frame_time == 0:
            self.next_frame()

    def next_frame(self):
        self.curr_frame += 1
        self.image = pygame.transform.scale(self.death_images[self.curr_frame], (self.MOB_SIZE, self.MOB_SIZE))

    #Actually running away from the player
    def move_because_of_player(self, chase:bool=False):
        super().move_because_of_player(chase)
    
    @staticmethod
    def check_group_attacked():
        return Fly.is_group_attacked

    @staticmethod
    def group_attacked():
        Fly.is_group_attacked = True
    
    @staticmethod
    def init_group_not_attacked():
        Fly.is_group_attacked = False