import random
from config import FPS
from entities.mobs.boss.boss_health_bar import BossHealthBar
from entities.mobs.boss.duke.duke import Duke
from entities.mobs.boss.husk.husk_animation import HuskAnimation
from entities.mobs.ghost import Ghost
from items.lootables.golden_coin import GoldenCoin
from items.lootables.pickup_heart import PickupHeart
from items.lootables.silver_coin import SilverCoin
from items.stat_items.categories import Categories
from items.stat_items.item import Item

class Husk(Duke):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.size = "Large"
        self._max_health = 40
        self._health = self._max_health
        self._damage = 1.5
        
        self.health_bar = BossHealthBar(game, self)
        self.moving_time_cd = int(0.7 * FPS)
        self.spawning_time_cd = int(3 * FPS)
        self.spawning_time =  self.spawning_time_cd
        #SKINS
        self.animation = HuskAnimation(self, game)
    
    def spawn_enemy(self):
        x = self.rect.centerx // self.game.settings.TILE_SIZE
        y = self.rect.centery // self.game.settings.TILE_SIZE
        room = self.game.map.get_current_room()
        x, y = self.rect.centerx//self.game.settings.TILE_SIZE, self.rect.centery//self.game.settings.TILE_SIZE
        room.spawn_mob(Ghost, x, y)
    
    def move_to_destination(self, speed_multiplier=3):
        return super().move_to_destination(speed_multiplier)
    
    def next_place_to_move(self):
        largest_x_possible, largest_y_possible = self.game.settings.MAP_WIDTH - 3, self.game.settings.MAP_HEIGHT - 3
        self.destination = random.randint(1, largest_x_possible), random.randint(1, largest_y_possible)

    def drop_lootable(self):
        for _ in range(7):
            self.room.items.append(SilverCoin(self.game, self.rect.centerx, self.rect.centery))

        for _ in range(5):
            self.room.items.append(GoldenCoin(self.game, self.rect.centerx, self.rect.centery))

        for _ in range(3):
            self.room.items.append(PickupHeart(self.game, self.rect.centerx, self.rect.centery))

        self.room.items.append(Item(self.game, self.rect.centerx, self.rect.centery, Categories.LEGENDARY, drop_animation=True, boss="husk"))