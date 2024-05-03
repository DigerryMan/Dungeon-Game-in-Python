import pygame
from config import FPS
from utils.directions import Directions
from map.destructable_block import DestructableBlock

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:Directions, speed=20, is_friendly=True, 
                 dmg=1, time_decay_in_seconds:float=0, additional_speed=0):
        #MAIN
        self.dmg = dmg
        self.direction = direction
        self.speed = speed * game.settings.SCALE
        self.is_friendly = is_friendly
        
        self.additional_speed = additional_speed
        self.time_decay = int(time_decay_in_seconds * FPS)
        self.time_left = self.time_decay
        self.game = game

        #SKIN
        self._layer = 2000
        self.color = self.get_right_color()
        self.image = game.image_loader.tears[self.color + "_tear"].copy()

        #HITBOX / POSITION
        self.BULLET_SIZE = self.game.settings.BULLET_SIZE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

        #DEATH ANIMATION
        self.is_alive = True
        self.frame = 0
        self.animation_time = 45
        self.time_per_frame = self.animation_time // 15

        #REST
        self.groups = self.game.all_sprites, self.game.attacks, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x_change = 0
        self.y_change = 0
        self.calculate_correct_speed()
        

    def get_right_color(self):
        if self.is_friendly:
            return "blue"
        return "red"

    def calculate_correct_speed(self):
        if self.direction == Directions.PLAYER: 
            self.calculate_speed_to_player()
        elif self.direction == Directions.ENEMY:
            self.calculate_speed_to_enemy()
        else:
            self.calculate_speed()

    def update(self):
        if self.is_alive:
            self.rect.x += self.x_change
            self.rect.y += self.y_change
            
            self.collide()
            if self.time_decay:
                self.decay()
            self._layer = self.rect.bottom + 2000
        
        else:
            self.animate_and_destroy()

    def calculate_speed(self):
        if(self.direction == Directions.UP):
            self.y_change = -self.speed
        elif(self.direction == Directions.DOWN):
            self.y_change = self.speed
        elif(self.direction == Directions.LEFT):
            self.x_change = -self.speed
        elif(self.direction == Directions.RIGHT):
            self.x_change = self.speed
        
        self.calculate_angled_speed()

    def calculate_angled_speed(self):
        axis, _ = self.direction.get_axis_tuple()
        if axis == 'x':
            self.y_change = self.additional_speed 
        elif axis == 'y':
            self.x_change = self.additional_speed
            
    def calculate_speed_to_player(self):
        player_vector = pygame.math.Vector2(self.game.get_player_rect().center)
        bullet_vector = pygame.math.Vector2(self.rect.center)
        distance = (player_vector - bullet_vector).magnitude()
        direction = None
        
        if distance > 0:
            direction = (player_vector - bullet_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        
        velocity = direction * self.speed
        self.x_change = int(velocity.x)
        self.y_change = int(velocity.y)

    def calculate_speed_to_enemy(self):
        self.enemies = self.game.enemies.sprites()
        closest_enemy = min(self.enemies, key=lambda enemy: pygame.math.Vector2(enemy.rect.center).distance_to(pygame.math.Vector2(self.rect.center)))

        enemy_vector = pygame.math.Vector2(closest_enemy.rect.center)
        bullet_vector = pygame.math.Vector2(self.rect.center)
        distance = (enemy_vector - bullet_vector).magnitude()
        direction = None

        if distance > 0:
            direction = (enemy_vector - bullet_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        velocity = direction * self.speed
        self.x_change = int(velocity.x)
        self.y_change = int(velocity.y)

    def collide(self):
        if self.is_friendly:       
            mob_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if mob_hits :
                mobs_to_get_hit = [mob_hit for mob_hit in mob_hits if self.get_mask_colliding_sprite([mob_hit])]
                for mob in mobs_to_get_hit:
                    if mob not in self.game.not_voulnerable:
                        mob_hits[0].get_hit(self.dmg)
                        self.is_alive = False
            
        else:
            player_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if player_hits:
                mask_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False, pygame.sprite.collide_mask)
                if mask_hits:  
                    player_hits[0].get_hit(self.dmg)
                    self.is_alive = False
            
        self.collide_blocks()
    
    def collide_blocks(self):
        door_hits = pygame.sprite.spritecollide(self, self.game.doors, False)
        if door_hits:
            mask_door_hit = self.get_mask_colliding_sprite(door_hits)
            if mask_door_hit:
                self.is_alive = False
            
        block_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
        if block_hits:
            mask_block_hits = [block_hit for block_hit in block_hits if self.get_mask_colliding_sprite([block_hit])]
            if mask_block_hits:
                self.is_alive = False
                for block_hit in mask_block_hits:
                    if isinstance(block_hit, DestructableBlock):
                        block_hit.get_hit()
                        
    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite

    def decay(self):
        self.time_left -= 1
        if self.time_left <= 0:
            self.is_alive = False

    def animate_and_destroy(self):
        if self.animation_time == 45:
            self.rect.x -= self.BULLET_SIZE
            self.rect.y -= self.BULLET_SIZE
            self.image = self.game.image_loader.tears[self.color + "_tear_pop" + str(self.frame)].copy()

        self.animation_time -= 1
        if self.animation_time % self.time_per_frame == 0:
            self.frame += 1
            self.image = self.game.image_loader.tears[self.color + "_tear_pop" + str(self.frame)].copy()

        if self.animation_time <= 0:
            self.kill()