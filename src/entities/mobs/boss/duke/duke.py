import random

import pygame

from config import FPS
from entities.mobs.boss.boss_health_bar import BossHealthBar
from entities.mobs.boss.duke.duke_animation import DukeAnimation
from entities.mobs.fly_aggresive import FlyAggresive
from entities.mobs.slime import Enemy
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin


class Duke(Enemy):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self.size = "Boss"
        self._max_health = 25
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)

        # CHANGED FROM ENEMY
        self.MOB_SIZE = int(game.settings.MOB_SIZE * 2.5)
        self.death_animator.scale_to_new_size(self.MOB_SIZE)
        # SKINS
        self.image = pygame.Surface([self.MOB_SIZE, self.MOB_SIZE])
        self.unchanged_image = self.image.copy()
        # HITBOX
        self.rect = self.image.get_rect()
        self.rect.centerx = x * game.settings.TILE_SIZE
        self.rect.centery = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        # REST
        self.is_spawning_mobs = False
        self.spawning_time_cd = int(1.5 * FPS)
        self.spawning_time = self.spawning_time_cd

        self.time_left_to_spawn_cd = int(1 * FPS)
        self.time_left_to_spawn = self.time_left_to_spawn_cd

        # MOVEMENT
        self.destination = None
        self.next_place_to_move()

        self.is_moving = False
        self.moving_time_cd = int(1.5 * FPS)
        self.moving_time = self.moving_time_cd
        # ANIMATION
        self.animation = DukeAnimation(self, game)

    def update(self):
        if not self._is_dead:
            self.collide_player()
            self.correct_layer()
            self.check_hit_and_animate()
            self.move()
            self.enemies_spawner()

        else:
            self.check_hit_and_animate()

    def enemies_spawner(self):
        if self.is_spawning_mobs:
            self.spawning_time -= 1
            if self.spawning_time <= 0:
                self.is_spawning_mobs = False
                self.spawning_time = self.spawning_time_cd
            elif self.spawning_time == self.spawning_time_cd // 2:
                self.spawn_enemy()
        else:
            self.time_left_to_spawn -= 1
            if self.time_left_to_spawn <= 0:
                self.is_spawning_mobs = True
                self.time_left_to_spawn = self.time_left_to_spawn_cd

    def next_place_to_move(self):
        largest_x_possible, largest_y_possible = (
            self.game.settings.MAP_WIDTH - 5,
            self.game.settings.MAP_HEIGHT - 5,
        )
        self.destination = random.randint(2, largest_x_possible), random.randint(
            2, largest_y_possible
        )

    def spawn_enemy(self):
        self.play_audio(f"dukeSpawnEnemy{random.randint(1,2)}")
        x = self.rect.centerx // self.game.settings.TILE_SIZE
        y = self.rect.centery // self.game.settings.TILE_SIZE
        room = self.game.map.get_current_room()
        x, y = (
            self.rect.centerx // self.game.settings.TILE_SIZE,
            self.rect.centery // self.game.settings.TILE_SIZE,
        )
        room.spawn_mob(FlyAggresive, x, y, self)

    def animate_alive(self):
        self.animation.animate()

    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)

    def correct_layer(self):
        self._layer = self.rect.centery

    def move(self):
        if self.is_moving:
            self.move_to_destination()
        else:
            self.moving_time -= 1
            if self.moving_time <= 0:
                self.is_moving = True
                self.play_audio("dukeMove")
                self.moving_time = self.moving_time_cd

    def move_to_destination(self, speed_multiplier=2):
        curr_x, curr_y = (
            self.rect.left // self.game.settings.TILE_SIZE,
            self.rect.top // self.game.settings.TILE_SIZE,
        )
        dest_x, dest_y = self.destination
        if curr_x == dest_x and curr_y == dest_y:
            self.is_moving = False
            self.next_place_to_move()
        else:
            x_speed, y_speed = (dest_x - curr_x) * speed_multiplier, (
                dest_y - curr_y
            ) * speed_multiplier
            self.rect.x += x_speed
            self.rect.y += y_speed

    def drop_lootable(self):
        drops = [SilverCoin] * 15 + [GoldenCoin] * 10 + [PickupHeart] * 2
        for drop in drops:
            self.room.items.append(
                drop(self.game, self.rect.centerx, self.rect.centery)
            )
