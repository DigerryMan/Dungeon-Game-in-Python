import random
from config import LIGHT_GREEN
from entities.bullet import Bullet
from entities.mobs.ghost import Ghost
from utils.directions import Directions
import pygame

class FriendlyGhost(Ghost):
    def __init__(self, game, x, y, reversed_moves=False):
        super().__init__(game, x, y)
        self._health = 3333
        self.damage = 1
        self.speed = 1 * game.settings.SCALE
        self._projectal_speed = 10
        self.reversed_moves = reversed_moves

        #ANIMATION
        self.next_frame_ticks_cd = 10
        self.time = 0

        self.MOB_SIZE = game.settings.MOB_SIZE
        self.img = None
        self.img = game.image_loader.get_image("friend_ghost")
        self.images = []
        self.frame = None
        self.which_frame = 0
        self.is_moving = False

        self.__prepare_images()
        self.image = self.images[0]

        #HITBOX
        self.mask = pygame.mask.from_surface(self.image)

        #REST
        self.groups = game.all_sprites, game.entities
        self.remove(game.enemies)

    def __prepare_images(self):
        mob_size = self.MOB_SIZE//2
        for y in range(3):
            for x in range(2):
                img = self.img.subsurface(pygame.Rect(x * self.MOB_SIZE, y * self.MOB_SIZE, self.MOB_SIZE, self.MOB_SIZE))
                self.images.append(pygame.transform.scale(img, (mob_size, mob_size)))
  
    def attack(self):
        self._shot_time_left -= 1
        if self._shot_time_left <= 0 and self.game.enemies:
            Bullet(self.game, self.rect.centerx, self.rect.centery, Directions.ENEMY, 
                   self._projectal_speed, True, self._damage, self._bullet_decay_sec)
            self.roll_next_shot_cd()
            self._shot_time_left = self._shot_cd
    
    def move_because_of_player(self, chase:bool=True):
        self.is_moving = False
        player_horizontal_facing = self.game.player.last_horizontall_facing
        player_rect = self.game.get_player_rect()
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = None

        left = player_rect.left + self.game.settings.PLAYER_SIZE//2
        right = player_rect.right
        if self.reversed_moves:
            left, right = right, left

        if player_horizontal_facing == Directions.LEFT:
            player_vector = pygame.math.Vector2(left, player_rect.top)
        else:
            player_vector = pygame.math.Vector2(right, player_rect.top)
            
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 3:
            self.is_moving = True
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

    def animate(self):
        if self.is_moving:
            self.time -= 1
            if self.time <= 0:
                self.time = self.next_frame_ticks_cd 
                self.which_frame += 1
                self.which_frame %= 2
        else:
            self.which_frame = 0

        self.next_frame()

    def next_frame(self):
        if self.is_moving:
            if self.facing == Directions.LEFT or self.facing == Directions.RIGHT:
                self.which_frame += 4
                if self.facing == Directions.RIGHT:
                    self.image = pygame.transform.flip(self.images[self.which_frame], True, False)
                    self.which_frame %= 2
                    return
            elif self.facing == Directions.UP:
                self.which_frame += 2
        self.image = self.images[self.which_frame]    
        self.which_frame = self.which_frame % 2