import pygame
from config import FPS, RED
from utils.directions import Directions

class Laser(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction:Directions, is_friendly=True, 
                 dmg=1, time_decay_in_seconds:float=0, opacity_time=0):
        #MAIN
        self.dmg = dmg
        self.direction = direction
        self.is_friendly = is_friendly
        self.opacity_time = int(opacity_time * FPS)
        self.width = 50
        self.height = 50

        self.time_decay = int(time_decay_in_seconds * FPS)
        self.time_left = self.time_decay
        self.game = game

        #SKIN
        self._layer = 1990
        self.images = []
        self.images_opacity = []

        #HITBOX / POSITION
        self.is_wrong = False
        self.rect = pygame.Rect(self.calculate_rect_cords(x, y), (self.width, self.height))
        if not self.is_wrong:
            self.prepare_images("laser", self.images)
            self.prepare_images("laser_opacity", self.images_opacity)

            self.image = self.images[0]
            self.mask = pygame.mask.from_surface(self.image)
            
            if self.opacity_time > 0:
                self.image = self.images_opacity[0]

            #DEATH ANIMATION
            self.is_alive = True
            self.frame = 0
            self.animation_time = 5
            self.animation_cd = 5

        #REST
        self.groups = self.game.all_sprites, self.game.attacks, self.game.entities
        pygame.sprite.Sprite.__init__(self, self.groups)
        if self.is_wrong:
            self.kill()

    def prepare_images(self, name:str, list:list):
        img = self.game.image_loader.others[name]
        for x in range(2):
            list.append(img.subsurface(pygame.Rect(x * 407, 0, 407, 906)))

        if self.direction == Directions.UP:
            for index, image in enumerate(list):
                list[index] = pygame.transform.rotate(image, 180)
        elif self.direction == Directions.RIGHT:
            #self.rect.width , self.rect.height = self.rect.height, self.rect.width
            for index, image in enumerate(list):
                list[index] = pygame.transform.rotate(image, 90)
        elif self.direction == Directions.LEFT:
            #self.rect.width , self.rect.height = self.rect.height, self.rect.width
            for index, image in enumerate(list):
                list[index] = pygame.transform.rotate(image, 270)

        for index, image in enumerate(list):
            list[index]= pygame.transform.scale(image, self.rect.size)

    def update(self):
        if self.opacity_time > 0:
            self.opacity_time -= 1
        else:  
            self.collide()
        self.decay()
        self.animate()
    
    def animate(self):
        self.animation_time -= 1
        if self.animation_time <= 0:
            self.frame += 1
            self.frame %= 2
            self.animation_time = self.animation_cd
            self.image = self.images[self.frame]
            if self.opacity_time > 0 :
                self.image = self.images_opacity[self.frame]

    def calculate_rect_cords(self, x, y):
        first_x_possible = self.game.settings.TILE_SIZE
        last_x_possible = self.game.settings.TILE_SIZE * (self.game.settings.MAP_WIDTH - 1)
        first_y_possible = self.game.settings.TILE_SIZE
        last_y_possible = self.game.settings.TILE_SIZE * (self.game.settings.MAP_HEIGHT - 1) + self.game.settings.TILE_SIZE // 2

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