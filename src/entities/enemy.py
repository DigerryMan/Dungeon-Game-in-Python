import random
from abc import ABC, abstractmethod

import pygame

from config import *
from entities.bullet import Bullet
from entities.enemy_collisions import EnemyCollisions
from entities.enemy_moves import EnemyMoves
from entities.mobs.death_animation import DeathAnimator
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from map.block import Block
from utils.directions import Directions
from utils.image_transformer import ImageTransformer


class Enemy(pygame.sprite.Sprite, ABC):
    is_group_attacked: bool = False

    def __init__(
        self,
        game,
        x: int,
        y: int,
        check_block_colisions: bool = True,
        is_wandering: bool = True,
        bullet_decay_sec: float = 0,
    ):
        self.game = game

        # CHANGEABLE STATS
        self._health = 4 * self.hp_scaling_factor()
        self._damage = 0.75 * self.dmg_scaling_factor()
        self._collision_damage = 1
        self.size = "Small"

        self._speed = (3 + (random.random() * 2 - 1)) * game.settings.SCALE
        self._chase_speed_debuff = 1
        self._projectal_speed = 10
        self._bullet_decay_sec = bullet_decay_sec
        self._shot_cd = int(2.5 * FPS)
        self._shot_time_left = self._shot_cd

        # POSITION
        self.MOB_SIZE = game.settings.MOB_SIZE
        self.x_change = 0
        self.y_change = 0

        # SKINS
        self.image = pygame.Surface([self.MOB_SIZE, self.MOB_SIZE])
        self.unchanged_image = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.frame = None
        self.images = []

        # HITBOX
        self.rect = self.image.get_rect()
        self.rect.x = x * game.settings.TILE_SIZE
        self.rect.y = y * game.settings.TILE_SIZE
        self._layer = self.rect.bottom

        # GETTING HIT ANIMATION
        self.hit_time_cd = int(0.1 * FPS)
        self.hit_time = 0
        self.is_change_of_frame = False

        # REST
        self.collisions_manager = EnemyCollisions(self, game, check_block_colisions)
        self.facing = random.choice([Directions.LEFT, Directions.RIGHT])

        self.death_animator = DeathAnimator(self, game)
        self.enemy_moves = EnemyMoves(self, game)
        self._is_wandering = is_wandering
        self._is_idling = self._is_wandering

        self._is_dead = False
        self.room = game.map.get_current_room()
        self.groups = self.game.all_sprites, self.game.enemies, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        if not self._is_dead:
            self.move()
            self.collide_player()
            if not self._is_wandering:
                self.attack()

            self.terrain_collisions()
            self.correct_facing()
            self.correct_layer()

        self.check_hit_and_animate()
        self.x_change = 0
        self.y_change = 0

    def terrain_collisions(self):
        self.collisions_manager.terrain_collisions()

    def check_hit_and_animate(self):
        if self.hit_time > 0:
            self.hit_time -= 1
            if self.hit_time == 0 and not self._is_dead:
                self.restore_image_colors()
        self.is_change_of_frame = False
        self.animate()
        if self.is_change_of_frame and self.hit_time > 0 and not self._is_dead:
            self.image = ImageTransformer.change_image_to_more_red(self.unchanged_image)

    def restore_image_colors(self):
        self.image = self.unchanged_image

    def move(self):
        if not self._is_dead:
            self.enemy_moves.move()

    def move_because_of_player(self, chase: bool = True):
        self.enemy_moves.move_because_of_player(chase)

    def collide_player(self):
        self.collisions_manager.collide_player()

    def attack(self):
        self._shot_time_left -= 1
        if self._shot_time_left <= 0:
            Bullet(
                self.game,
                self.rect.centerx,
                self.rect.centery,
                Directions.PLAYER,
                self._projectal_speed,
                False,
                self._damage,
                self._bullet_decay_sec,
            )
            self.roll_next_shot_cd()
            self._shot_time_left = self._shot_cd

    def collide_blocks(self, orientation: str):
        self.collisions_manager.collide_blocks(orientation)

    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if isinstance(sprite, Block):
                block_surface = pygame.Surface((sprite.rect.width, sprite.rect.height))
                block_mask = pygame.mask.from_surface(block_surface)
                offset_x = sprite.rect.x - self.rect.x
                offset_y = sprite.rect.y - self.rect.y
                if self.mask.overlap(block_mask, (offset_x, offset_y)):
                    return sprite

            if pygame.sprite.collide_mask(self, sprite):
                return sprite

    def _correct_rounding(self):
        self.x_change += 1 if self.x_change >= 0 else -1
        self.y_change += 1 if self.y_change >= 0 else -1

    def correct_facing(self):
        self.enemy_moves.correct_facing()

    def get_hit(self, dmg: int):
        if self not in self.game.not_voulnerable:
            self.play_hit_sound()
            self._health -= dmg
            self._is_wandering = False
            self.group_attacked()
            self.check_if_dead()

            self.hit_time = self.hit_time_cd
            if not self._is_dead:
                self.image = ImageTransformer.change_image_to_more_red(
                    self.unchanged_image
                )

    def play_hit_sound(self):
        self.play_audio(f"enemyHit{random.randint(1, 3)}")

    def play_audio(self, audio: str):
        self.game.sound_manager.play(audio)

    def check_if_dead(self):
        if self._health <= 0:
            self.start_dying()

    def roll_next_shot_cd(self):
        self._shot_cd = random.randint(int(1.5 * FPS), int(3 * FPS))

    def correct_layer(self):
        self._layer = self.rect.bottom

    def start_dying(self, instant_death=False):
        self._is_dead = True
        self.play_death_sound()
        self.drop_lootable()
        if instant_death:
            self.final_death()
        else:
            self.game.not_voulnerable.add(self)

    def final_death(self):
        self.kill()

    def drop_lootable(self):
        if DROP_LOOT_EVERYTIME:  # FOR TESTING PURPOSES!
            self.room.items.append(
                Item(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    Categories.VERY_COMMON,
                )
            )
        else:
            if random.random() < 0.3:  # chance to have any drop at all
                if (
                    random.random() < 0.7
                ):  # chance to have a lootable (coin, heart, etc.)
                    if random.random() < 0.5:
                        self.room.items.append(
                            SilverCoin(self.game, self.rect.centerx, self.rect.centery)
                        )
                    elif random.uniform(0, 0.5) < 0.3:
                        self.room.items.append(
                            GoldenCoin(self.game, self.rect.centerx, self.rect.centery)
                        )
                    else:
                        self.room.items.append(
                            PickupHeart(self.game, self.rect.centerx, self.rect.centery)
                        )
                else:
                    self.room.items.append(
                        Item(
                            self.game,
                            self.rect.centerx,
                            self.rect.centery,
                            Categories.VERY_COMMON,
                        )
                    )

    def draw_additional_images(self, screen):
        pass

    def animate(self):
        if not self._is_dead:
            self.animate_alive()
        else:
            self.animate_dead()

    @abstractmethod
    def animate_alive(self):
        pass

    def animate_dead(self):
        self.death_animator.death_animation()

    @staticmethod
    def check_group_attacked():
        return Enemy.is_group_attacked

    @staticmethod
    def group_attacked():
        Enemy.is_group_attacked = True

    def get_bombed(self):
        self.get_hit(1)

    def play_death_sound(self):
        if self.size == "Large":
            self.game.sound_manager.play(f"Death_Burst_Large_{random.randint(0, 1)}")
        elif self.size == "Small":
            self.game.sound_manager.play(f"Death_Burst_Small_{random.randint(0, 2)}")
        elif self.size == "Boss":
            self.game.sound_manager.play("boss_death")

    def hp_scaling_factor(self):
        return 1 + 2 * (self.game.map.get_current_room().level - 1) / 7

    def dmg_scaling_factor(self):
        return 1 + (self.game.map.get_current_room().level - 1) / 7
