import random
import pygame
from config import BASE_IMMORTALITY_AFTER_HIT, BASE_LUCK, BASE_SHOOTING_COOLDOWN, BASE_SHOT_SPEED, FPS, GOD_MODE, ROOM_NUMBER
from entities.bomb import Bomb
from entities.mobs.friendly_ghost import FriendlyGhost
from entities.player.equipment.equipment import Equipment
from entities.player.player_animation import PlayerAnimation
from entities.player.player_collisions import PlayerCollisionEngine
from entities.player.player_shooting_engine import ShootingEnginge
from entities.player.player_types import PlayerTypes
from utils.directions import Directions

class Player(pygame.sprite.Sprite):
    direction_mapping = {
            pygame.K_a: (Directions.LEFT, -1, 0),
            pygame.K_d: (Directions.RIGHT, 1, 0),
            pygame.K_w: (Directions.UP, 0, -1),
            pygame.K_s: (Directions.DOWN, 0, 1)
        }
    def __init__(self, game, x, y, player_type=PlayerTypes.ISAAC):
        #MAIN
        self.game = game
        self.player_type = player_type
        self.BASE_MAX_HEALTH, self.dmg, self.BASE_SPEED = self.player_type.get_player_stats()
        self.max_health = self.BASE_MAX_HEALTH 
        self.speed = self.BASE_SPEED * game.settings.SCALE

        self.health = self.max_health
        self.PLAYER_SIZE = game.settings.PLAYER_SIZE
        self.coins = 0
        self.bombs = 5
        self.rooms_cleared = 0
        
        #SKIN
        self.animation = PlayerAnimation(game, self, player_type)
        self.image = self.animation.image
        self._layer = self.image.get_rect().bottom

        #HITBOX / POSITION
        self.rect = self.image.get_rect()
        self.rect.x = x * self.PLAYER_SIZE
        self.rect.y = y * self.PLAYER_SIZE
        self.collisions = PlayerCollisionEngine(game, self)
        
        #MOVEMENT
        self.x_change = 0
        self.y_change = 0
        self.is_moving = False

        #DIRECTION
        self.facing = Directions.DOWN
        self.direction = Directions.DOWN
        self.last_horizontall_facing = Directions.RIGHT

        #EQ
        self.eq = Equipment(self, game)
        self.eq_opened = False

        #SHOOTING
        self.shooting_engine = ShootingEnginge(self, game)

        #REST
        self.is_alive = True
        self.end_of_death_animation = False
        self.immortality_time_left = 0

        self.groups = self.game.all_sprites, self.game.player_sprite, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.mask = self.animation.get_init_mask()
    

    def update(self):
        if self.is_alive:
            self.user_input()
            self.collisions.correct_unvalid_move()
            self.collisions.check_items_pick_up()
            
            self._layer = self.rect.bottom
            self.image = self.animation.animate_and_get_image()

            self.immortality_time_left -= 1
            self.x_change = 0
            self.y_change = 0
        else:
            if not self.end_of_death_animation:
                self.animation.play_death_animation() 
            else:
                self.game.game_over()
        
    def user_input(self):
        keys = pygame.key.get_pressed()
        x_y_vel = [0,0]
        self.is_moving = False
        self.move(keys, x_y_vel)
        self.plant_bomb(x_y_vel)
        self.shoot(keys, x_y_vel)

    def move(self, keys, x_y_vel):
        for key in self.direction_mapping:
            if keys[key]:
                self.direction, x_change, y_change = self.direction_mapping[key]
                self.x_change += int(self.speed) * x_change
                self.y_change += int(self.speed) * y_change
                self.facing = self.direction
                if self.direction in [Directions.LEFT, Directions.RIGHT]:
                    self.last_horizontall_facing = self.direction
                x_y_vel[0] += x_change
                x_y_vel[1] += y_change
                self.is_moving = True
        
        self.correct_diagonal_movement()

    def plant_bomb(self, x_y_vel):
        if self.game.e_pressed and self.bombs > 0:
            if self.facing == Directions.LEFT or x_y_vel[0] < 0:
                Bomb(self.game, self.rect.centerx, self.rect.centery, rotate = True)
            else:
                Bomb(self.game, self.rect.centerx, self.rect.centery)
            self.bombs -= 1

    def shoot(self, keys, x_y_vel):
        self.shooting_engine.shoot(keys, x_y_vel)

    def correct_diagonal_movement(self):
        if(self.x_change and self.y_change):
            self.x_change //= 1.41
            self.y_change //= 1.41
            if self.x_change < 0:
                self.x_change += 1
            if self.y_change < 0:
                self.y_change += 1

    def get_center_position(self):
        return self.rect.centerx, self.rect.centery
    
    def set_rect_position(self, x_rect, y_rect):
        self.rect.x = x_rect
        self.rect.y = y_rect

    def get_hit(self, dmg:int):
        if self.immortality_time_left <= 0:
            self.health -= dmg * (1 - self.eq.stats["dmg_reduction"]) * self.eq.extra_stats["dmg_taken_multiplier"]
            self.health = round(self.health, 2)
            self.immortality_time_left = self.get_immortality_time()
            self.check_is_dead()

    def check_is_dead(self):
        if self.health <= 0 and not GOD_MODE:
            self.is_alive = False
            self.game.sound_manager.play("isaacDeath")

        else:
            self.game.sound_manager.play(f"hurt{random.randint(1, 3)}")
    
    def heal(self, amount:int):
        if amount < 0:  
            raise ValueError("Healing amount must be positive")
        self.health = min(self.max_health, self.health + amount)
        self.game.sound_manager.play("heartIntake")
    
    def get_shooting_cooldown(self):
        return int((BASE_SHOOTING_COOLDOWN - self.eq.stats["shooting_cooldown"]) * FPS)

    def get_immortality_time(self):
        return int((BASE_IMMORTALITY_AFTER_HIT + self.eq.stats["immortality"]) * FPS)

    def get_shot_speed(self):
        return BASE_SHOT_SPEED + self.eq.stats["shot_speed"]
    
    def get_luck(self):
        return BASE_LUCK + self.eq.stats["luck"]
    
    def spawn_pets(self, is_in_new_room:bool=True):
        pets_to_spawn = self.eq.extra_stats.get("friendly_ghost")
        if not is_in_new_room:
            FriendlyGhost(self.game, self.rect.centerx//self.game.settings.TILE_SIZE, 
                          self.rect.centery//self.game.settings.TILE_SIZE, pets_to_spawn%2!=1)
        else:
            for i in range(pets_to_spawn):
                FriendlyGhost(self.game, self.rect.centerx//self.game.settings.TILE_SIZE, 
                              self.rect.centery//self.game.settings.TILE_SIZE, i%2==1)
   
    def update_rooms_cleared(self):
        self.rooms_cleared += 1
        self.rooms_cleared = min(self.rooms_cleared, ROOM_NUMBER - 2)
    
    def prepare_for_next_map(self):
        self.rooms_cleared = 0

    def get_bombed(self):
        self.get_hit(1)