import pygame
import random

class LootableItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y, drop_animation=True):
        self.game = game
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface([30, 30])
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self._layer = self.rect.centery

        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.is_picked_up = False

        if drop_animation:
            TS = game.settings.TILE_SIZE
            self.drop_animation_time = 40
            self.horizontal_velocity = random.uniform(-3, 3) * game.settings.SCALE

            x = self.horizontal_velocity * self.drop_animation_time
            y = -(((5/4) * TS**2 - x**2)**0.5)

            final_y = y + self.y + TS//4

            self.acceleration = 0.5 * game.settings.SCALE
            self.vertical_velocity = -((self.y - final_y - (self.acceleration * self.drop_animation_time**2)/2) / self.drop_animation_time)
            self.vertical_velocity *= random.uniform(0.95, 1.05)

            self.vertical_velocity_multiplier = -1
            self.horizontal_velocity_multiplier = 1

        else:
            self.drop_animation_time = 0


    def update(self):
        self._layer = self.rect.centery
        self.drop_animation()
        
    def drop_animation(self):
        if self.drop_animation_time > 0:
            self.vertical_velocity -= self.acceleration
            self.update_position()
            self.drop_animation_time -= 1

    def update_position(self):
        def collide_blocks(orientation:str):
            nonlocal x_change, y_change
            rect_hits = pygame.sprite.spritecollide(self, self.game.collidables, False)
            if rect_hits:
                mask_hits = get_mask_colliding_sprite(rect_hits)
                if mask_hits:
                    if orientation == 'x':
                        self.x -= x_change
                        self.rect.x = round(self.x)
                        self.horizontal_velocity_multiplier *= -1
                    elif orientation == 'y':
                        self.y -= y_change
                        self.rect.y = round(self.y)
                        self.vertical_velocity = 0

        def get_mask_colliding_sprite(rect_hits):
            for sprite in rect_hits:
                if sprite.__class__.__name__ == 'Chest':
                    continue
                    
                if pygame.sprite.collide_mask(self, sprite):
                    return sprite
                
        x_change = self.horizontal_velocity * self.horizontal_velocity_multiplier
        y_change = self.vertical_velocity * self.vertical_velocity_multiplier

        self.x += x_change
        self.rect.x = round(self.x)
        collide_blocks('x')
        self.y += y_change
        self.rect.y = round(self.y)
        collide_blocks('y')

        self._layer = 10000

    def picked_up(self):
        pass
    
    def clean_up(self):
        current_room = self.game.map.get_current_room()
        current_room.remove_item(self)