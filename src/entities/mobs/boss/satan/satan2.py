import random

from entities.bullet import Bullet
from entities.mobs.boss.boss_health_bar import BossHealthBar
from entities.mobs.boss.satan.satan import Satan
from entities.mobs.boss.satan.satan_animation import SatanAnimiation
from utils.directions import Directions


class Satan2(Satan):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self._max_health = 70
        self._health = self._max_health
        self._damage = 1

        self.health_bar = BossHealthBar(game, self)
        self.animation = SatanAnimiation(self, game, "satan2")

        self.fly_speed = round(10 * self.game.settings.SCALE)
        self.max_mouth_attacks = 1

    def mouth_attack(self):
        for _ in range(12):
            x = self.rect.centerx + random.randint(-2, 2)
            y = self.rect.centery + int(self.MOB_HEIGHT * 0.3)
            decay = random.random() * 0.3 + 0.5
            speed = random.randint(17, 21)

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

        self.mouth_attack_amount += 1

    def next_move_type(self, to_exclude: str = ""):
        moves = {
            (0.00, 0.34): "bullets_from_hands",
            (0.35, 0.69): "mouth_attack",
            (0.70, 0.84): "laser_breath",
            (0.85, 1.00): "flying",
        }
        move = to_exclude
        while move == to_exclude:
            rolled = random.random()
            for move_range, move_name in moves.items():
                if move_range[0] <= rolled <= move_range[1]:
                    move = move_name

        if move == "bullets_from_hands":
            self.bullets_from_hands_active = True
        elif move == "laser_breath":
            self.laser_breath_active = True
        elif move == "mouth_attack":
            self.mouth_attack_active = True
        elif move == "flying":
            self.flying_active = True

    def spawn_projectiles_in_circle(self, x, y, more_to_right=False):
        bullet_velocity = 20
        angles = [x for x in range(-25, 191, 18)]
        if more_to_right:
            angles = [-alpha for alpha in angles]

        for alpha in angles:
            v_x, v_y = self.calculate_rigth_speed(bullet_velocity, alpha)
            Bullet(self.game, x, y, Directions.UP, v_y, False, 1, 0, v_x)

    def drop_lootable(self):
        pass
