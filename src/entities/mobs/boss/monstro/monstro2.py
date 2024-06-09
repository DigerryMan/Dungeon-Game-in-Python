import random

from config import FPS
from entities.bullet import Bullet
from entities.mobs.boss.boss_health_bar import BossHealthBar
from entities.mobs.boss.monstro.monstro import Monstro
from entities.mobs.boss.monstro.monstro_animation import MonstroAnimation
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from utils.directions import Directions


class Monstro2(Monstro):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self._max_health = 400
        self._health = self._max_health
        self._damage = 1.75
        self._projectal_speed = 11

        self.health_bar = BossHealthBar(game, self)

        # ANIMATION
        self.animation = MonstroAnimation(self, game, "monstro2")

        # BOSS STAGES
        self.stage = 1

        self.is_doing_bullet_attack = False
        self.bullet_direction = None
        self.bullet_shooting_cd = 0.5 * FPS
        self.bullet_shooting_time_left = self.bullet_shooting_cd

        self.jump_cd_s = 0.75
        self.jump_cd = self.jump_cd_s * FPS

        self.max_number_of_jumps = 2
        self.number_of_jumps = 0
        self.stage_1_time = None

    def shoot_one_of_crazy_bullets(self):
        for _ in range(11):
            x, y = self.rect.centerx + random.randint(
                -12, 12
            ), self.rect.centery + random.randint(-12, 12)
            decay = random.random() * 0.25 + 0.4
            speed = random.randint(18, 23)
            additional_speed = random.randint(-4, 4)
            Bullet(
                self.game,
                x,
                y,
                Directions.PLAYER,
                speed,
                False,
                self._damage,
                decay,
                additional_speed,
            )

        self.game.sound_manager.play(f"tear{random.randint(1, 2)}")

    def drop_lootable(self):
        drops = [SilverCoin] * 15 + [GoldenCoin] * 10 + [PickupHeart] * 3
        for drop in drops:
            self.room.items.append(
                drop(self.game, self.rect.centerx, self.rect.centery)
            )
