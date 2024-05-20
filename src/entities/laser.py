import pygame
from config import FPS, RED
from utils.directions import Directions

class Laser(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:Directions, is_friendly=True, 
                 dmg=1, time_decay_in_seconds:float=0):
        #MAIN
        self.dmg = dmg
        self.direction = direction
        self.is_friendly = is_friendly
        
        self.width = 50
        self.height = 50

        self.time_decay = int(time_decay_in_seconds * FPS)
        self.time_left = self.time_decay
        self.game = game

        #SKIN
        self._layer = 1990

        #HITBOX / POSITION
        self.is_wrong = False
        self.rect = pygame.Rect(self.calculate_rect_cords(x, y), (self.width, self.height))
        if not self.is_wrong:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(RED)
            self.mask = pygame.mask.from_surface(self.image)

            #DEATH ANIMATION
            self.is_alive = True
            self.frame = 0
            self.animation_time = 30
            self.time_per_frame = self.animation_time // 15

        #REST
        self.groups = self.game.all_sprites, self.game.attacks, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)
        if self.is_wrong:
            self.kill()

    def update(self):
        self.collide()
        self.decay()

    def calculate_rect_cords(self, x, y):
        first_x_possible = self.game.settings.TILE_SIZE
        last_x_possible = self.game.settings.TILE_SIZE * (self.game.settings.MAP_WIDTH - 1)
        first_y_possible = self.game.settings.TILE_SIZE
        last_y_possible = self.game.settings.TILE_SIZE * (self.game.settings.MAP_HEIGHT - 1)

        new_x, new_y = 0, 0
        if self.direction == Directions.LEFT:
            new_x = first_x_possible
            new_y = y - self.height // 2
            self.width = x - new_x
        elif self.direction == Directions.RIGHT:
            new_x = x
            new_y = y - self.height // 2
            self.width = last_x_possible - x

        elif self.direction == Directions.UP:
            new_x = x - self.width // 2
            new_y = first_y_possible
            self.height = y - first_y_possible

        elif self.direction == Directions.DOWN:
            new_x = x - self.width // 2
            new_y = y
            self.height = last_y_possible - y
        
        if self.width <= 0 or self.height <= 0:
            self.is_wrong = True

        return new_x, new_y

    def collide(self):
        if self.is_friendly:       
            mob_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if mob_hits :
                mobs_to_get_hit = [mob_hit for mob_hit in mob_hits if self.get_mask_colliding_sprite([mob_hit])]
                for mob in mobs_to_get_hit:
                    if mob not in self.game.not_voulnerable:
                        mob_hits[0].get_hit(self.dmg)
            
        else:
            player_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if player_hits:
                mask_hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False, pygame.sprite.collide_mask)
                if mask_hits:  
                    player_hits[0].get_hit(self.dmg)

    def decay(self):
            self.time_left -= 1
            if self.time_left <= 0:
                self.kill()
    
    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite