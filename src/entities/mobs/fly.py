import random

import pygame

from config import FPS
from entities.enemy import Enemy


class Fly(Enemy):
    is_group_attacked = False

    def __init__(self, game, x: int, y: int, wanders=True):
        super().__init__(
            game,
            x,
            y,
            check_block_colisions=True,
            is_wandering=wanders,
            bullet_decay_sec=2.0,
        )
        # CHANGEABLE STATS
        self._health = 4
        self._speed = 1 * game.settings.SCALE
        self._projectal_speed = 6
        self._shot_cd = int(2.4 * FPS)

        # SKIN
        self.curr_frame = 0
        self.next_frame_ticks_cd = 3
        self.time = self.next_frame_ticks_cd
        self.next_frame_time = 3
        self.dead_animation_time = 10 * self.next_frame_time
        self.dead_animation_time_left = self.dead_animation_time

        self.img = game.image_loader.get_image("fly")
        self.prepare_images()

        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        Fly.init_group_not_attacked()

    def prepare_images(self):
        multi = random.randint(0, 2)
        for x in range(multi, 2 + multi):
            self.images.append(
                self.img.subsurface(
                    pygame.Rect(x * self.MOB_SIZE, 0, self.MOB_SIZE, self.MOB_SIZE)
                )
            )

        self.death_animator.prepare_death_images_for_fly()

    def collide_blocks(self, orientation: str):
        rect_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if rect_hits:
            if orientation == "x":
                self.rect.x -= self.x_change

            if orientation == "y":
                self.rect.y -= self.y_change

    def animate_alive(self):
        if not self._is_dead:
            self.time -= 1
            if self.time < 0:
                self.is_change_of_frame = True
                self.curr_frame = (self.curr_frame + 1) % 2
                self.image = self.images[self.curr_frame]
                self.unchanged_image = self.image.copy()
                self.time = self.next_frame_ticks_cd
        else:
            self.death_animator.death_animation()

    def start_dying(self):
        super().start_dying(False)

    # Actually running away from the player
    def move_because_of_player(self, chase: bool = False):
        super().move_because_of_player(chase)

    def attack(self):
        if not self._is_dead:
            super().attack()

    @staticmethod
    def check_group_attacked():
        return Fly.is_group_attacked

    @staticmethod
    def group_attacked():
        Fly.is_group_attacked = True

    @staticmethod
    def init_group_not_attacked():
        Fly.is_group_attacked = False
