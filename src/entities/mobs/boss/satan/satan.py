import math
import random
from cmath import cos, sin

import pygame

from config import FPS
from entities.bullet import Bullet
from entities.laser import Laser
from entities.mobs.boss.boss_health_bar import BossHealthBar
from entities.mobs.boss.satan.satan_animation import SatanAnimiation
from entities.mobs.slime import Enemy
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item
from utils.directions import Directions


class Satan(Enemy):
    moves = ["bullets_from_hands", "laser_breath", "mouth_attack", "flying"]

    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self.size = "Boss"
        self._max_health = 50
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)
        # CHANGED FROM ENEMY
        self.MOB_WIDTH = game.settings.MOB_SIZE * 5
        self.MOB_HEIGHT = int(game.settings.MOB_SIZE * 3.5)
        self.death_animator.scale_to_new_size_v2(self.MOB_WIDTH, self.MOB_HEIGHT)

        # SKINS
        self.image = pygame.Surface([self.MOB_WIDTH, self.MOB_HEIGHT])

        # HITBOX
        self.rect = self.image.get_rect()
        self.rect.centerx = x * game.settings.TILE_SIZE
        self.rect.centery = y * game.settings.TILE_SIZE - int(self.MOB_HEIGHT * 0.8)
        self._layer = self.rect.bottom

        # START
        self.boss_figth_start_active = True
        self.start_time = 3 * FPS
        self.game.not_voulnerable.add(self)

        # HANDS BULLETS
        self.bullets_from_hands_active = False
        self.bullets_from_hands_period = int(1 * FPS)
        self.bullets_from_hands_time = self.bullets_from_hands_period

        # LASER BREATH
        self.laser = None
        self.laser_breath_active = False
        self.laser_breath_period = int(1 * FPS)
        self.laser_breath_time = self.laser_breath_period

        # MOUTH ATTACK
        self.mouth_attack_active = False
        self.mouth_attack_period = int(1 * FPS)
        self.mouth_attack_time = self.mouth_attack_period
        self.max_mouth_attacks = 2
        self.mouth_attack_amount = 0

        # FLYING
        self.flying_active = False
        self.flying_period = int(1.5 * FPS)
        self.flying_time = self.flying_period
        self.first_short_fly = True
        self.fly_multiplier = 1
        self.fly_speed = round(9 * self.game.settings.SCALE)

        # ANIMATION
        self.animation = SatanAnimiation(self, game)

    def draw_additional_images(self, screen):
        self.health_bar.draw(screen)

    def animate_alive(self):
        self.animation.animate()

    def update(self):
        if not self._is_dead:
            self.perform_boss_stage()
            self.collide_player()
            self.correct_layer()
        self.check_hit_and_animate()

    def perform_boss_stage(self):
        if self.boss_figth_start_active:
            self.boss_figth_start_stage()
        elif self.bullets_from_hands_active:
            self.bullets_from_hands_stage()
        elif self.laser_breath_active:
            self.laser_breath_stage()
        elif self.mouth_attack_active:
            self.mouth_attack_stage()
        elif self.flying_active:
            self.flying_stage()

    def flying_stage(self):
        if self.flying_time == self.flying_period:
            self.play_audio("satanFly")
        self.fly()

    def mouth_attack_stage(self):
        if self.mouth_attack_time == self.mouth_attack_period:
            self.play_audio("satanShoot")
        self.mouth_attack_time -= 1
        if self.mouth_attack_time == int(self.mouth_attack_period * 0.55):
            self.mouth_attack()
        elif self.mouth_attack_time <= 0:
            self.mouth_attack_time = self.mouth_attack_period
            if self.mouth_attack_amount == self.max_mouth_attacks:
                self.mouth_attack_active = False
                self.mouth_attack_amount = random.randint(-1, 0)
                self.next_move_type("mouth_attack")

    def laser_breath_stage(self):
        if self.laser_breath_time == self.laser_breath_period:
            self.play_audio("satanLaser")
        self.laser_breath_time -= 1
        if self.laser_breath_time == int(self.laser_breath_period * 0.75):
            self.laser_breath_attack()
        elif self.laser_breath_time == int(self.laser_breath_period * 0.42):
            self.laser.kill()
            self.laser = None
        elif self.laser_breath_time <= 0:
            self.laser_breath_time = self.laser_breath_period
            self.laser_breath_active = False
            self.next_move_type("laser_breath")

    def bullets_from_hands_stage(self):
        if self.bullets_from_hands_time == self.bullets_from_hands_period:
            self.play_audio("satanShootHands")
        self.bullets_from_hands_time -= 1
        if self.bullets_from_hands_time == self.bullets_from_hands_period // 2:
            self.bullets_from_hands_attack()
        elif self.bullets_from_hands_time <= 0:
            self.bullets_from_hands_time = self.bullets_from_hands_period
            self.bullets_from_hands_active = False
            self.next_move_type()

    def boss_figth_start_stage(self):
        if self.start_time == 3 * FPS:
            self.play_audio_with_fadein("satanFound", 1000)
        self.start_time -= 1
        if self.start_time <= 0:
            self.play_audio("satanAppear"),
            self.boss_figth_start_active = False
            self.bullets_from_hands_active = True
            self.game.not_voulnerable.remove(self)

    def fly(self):
        self.flying_time -= 1
        speed = self.fly_speed * self.fly_multiplier
        if self.first_short_fly:
            speed /= 2
        self.rect.x += speed
        if self.flying_time <= 0:
            self.fly_multiplier *= -1
            self.flying_time = self.flying_period
            self.first_short_fly = False
            self.flying_active = False
            self.next_move_type("flying")

    def next_move_type(self, to_exclude: str = ""):
        try:
            moves_copy = Satan.moves.copy()
            moves_copy.remove(to_exclude)
        except ValueError:
            pass
        move = random.choice(moves_copy)
        if move == "bullets_from_hands":
            self.bullets_from_hands_active = True
        elif move == "laser_breath":
            self.laser_breath_active = True
        elif move == "mouth_attack":
            self.mouth_attack_active = True
        elif move == "flying":
            self.flying_active = True

    def mouth_attack(self):
        x, y = self.rect.centerx, self.rect.centery + int(self.MOB_HEIGHT * 0.3)
        for i in range(0, 9, 2):
            Bullet(self.game, x, y, Directions.PLAYER, 9 + i, False, 1, 1)
        self.mouth_attack_amount += 1

    def laser_breath_attack(self):
        x, y = self.rect.centerx, self.rect.centery + int(self.MOB_HEIGHT * 0.12)
        self.laser = Laser(self.game, x, y, Directions.DOWN, False, 1, 1)

    def bullets_from_hands_attack(self):
        x, y = self.rect.centerx, self.rect.centery
        self.spawn_projectiles_in_circle(
            int(x + self.MOB_WIDTH * 0.35), int(y + self.MOB_HEIGHT * 0.1), True
        )
        self.spawn_projectiles_in_circle(
            int(x - self.MOB_WIDTH * 0.35), int(y + self.MOB_HEIGHT * 0.1), False
        )

    def spawn_projectiles_in_circle(self, x, y, more_to_right=False):
        bullet_velocity = 20
        angles = [x for x in range(-14, 191, 29)]
        if more_to_right:
            angles = [-alpha for alpha in angles]

        for alpha in angles:
            v_x, v_y = self.calculate_rigth_speed(bullet_velocity, alpha)
            Bullet(self.game, x, y, Directions.UP, v_y, False, 1, 0, v_x)

    def calculate_rigth_speed(self, v_x_y: int, alpha: int):
        v_y = v_x_y * cos(math.radians(alpha)).real
        v_x = v_x_y * sin(math.radians(-alpha)).real
        v_x_balance = abs(v_x / v_x_y) / 2
        return v_x * v_x_balance, v_y

    def do_to_player_jumps_stage1(self):
        self.move()
        self.attack()

    def start_dying(self):
        self._is_dead = True
        if self.laser is not None:
            self.laser.kill()
        self.drop_lootable()
        self.game.sound_manager.play("enemyDeath")
        self.game.not_voulnerable.add(self)

    def drop_lootable(self):
        drops = [SilverCoin] * 10 + [GoldenCoin] * 5 + [PickupHeart] * 3
        for drop in drops:
            self.room.items.append(
                drop(self.game, self.rect.centerx, self.rect.centery)
            )

        self.room.items.append(
            Item(
                self.game,
                self.rect.centerx,
                self.rect.centery,
                Categories.LEGENDARY,
                boss="satan",
            )
        )

    def play_audio_with_fadein(self, audio: str, time_ms):
        self.game.sound_manager.play_with_fadein(audio, time_ms)

    def play_hit_sound(self):
        self.play_audio("satanHit")
