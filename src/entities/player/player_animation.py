import pygame
from utils.directions import Directions

class PlayerAnimation():
    def __init__(self, game, player, player_type):
        self.game = game
        self.player = player
        self.player_type = player_type
        self.PLAYER_SIZE = self.player.PLAYER_SIZE

        self.img = game.image_loader.get_image(player_type.value)
        self.body_images = []
        self.head_images = []
        self.prepare_images()
        self.frame = None
        self.image = self.body_images[0]

        self.intro_image = None
        self.intro_name = None
        self.prepare_intro_images()

        #ANIMATION
        self.x_legs_frame = 0
        self.body_frame = None
        self.reversed_body_frame = False
        self.x_head_frame = 0
        self.head_frame = None
        self.reversed_head = False
        self.head_tear_anime_cd = 4
        self.head_tear_anime_time_left = -1
        self.next_frame_ticks_cd = 3
        self.time = 0
        
        #DEATH ANIMATION
        self.death_frame_cd = 12
        self.death_time_left = self.death_frame_cd
        self.death_index = 0
        self.last_death_index = 4

    def prepare_images(self):
        for y in range(1, 3):
            for x in range(10):
                self.body_images.append(self.img.subsurface(pygame.Rect(x * self.PLAYER_SIZE, y * self.PLAYER_SIZE, self.PLAYER_SIZE, self.PLAYER_SIZE)))

        for x in range(6):
            self.head_images.append(self.img.subsurface(pygame.Rect(x * self.PLAYER_SIZE, 0, self.PLAYER_SIZE, self.PLAYER_SIZE)))

    def prepare_intro_images(self):
        img = self.game.image_loader.images_dict[f"{self.player_type.value}_display"]["boss_intro"]["image"]
        self.intro_image = pygame.transform.scale(img, (img.get_width() * 4 * self.game.settings.SCALE, img.get_height() * 4 * self.game.settings.SCALE))
        img = self.game.image_loader.images_dict[f"{self.player_type.value}_display"]["boss_intro"]["name"]
        self.intro_name = pygame.transform.scale(img, (img.get_width() * 4 * self.game.settings.SCALE, img.get_height() * 4 * self.game.settings.SCALE))
    
    def animate_and_get_image(self):
        self.animate()
        return self.image

    def reset_tear_shot_cd(self):
        self.head_tear_anime_time_left = self.head_tear_anime_cd

    def animate(self):
        self.reversed_body_frame = False
        if self.player.is_moving:
            self.time -= 1
        
        if self.time <= 0:
            self.time = self.next_frame_ticks_cd 
            self.x_legs_frame = (self.x_legs_frame + 1) % 10
        
        self.set_body_frame()
        if not self.player.is_moving:
            self.set_standing_frame()

        self.check_tear_animation()
        self.set_head_frame()
        self.next_frame()
    
    def check_tear_animation(self):
        self.head_tear_anime_time_left -= 1
        if self.head_tear_anime_time_left == self.head_tear_anime_cd - 1 or self.head_tear_anime_time_left == 1:
            self.x_head_frame = (self.x_head_frame + 1) % 2

    def set_standing_frame(self):
        self.body_frame = self.body_images[0]

    def next_frame(self):
        self.frame = pygame.Surface((self.PLAYER_SIZE, self.PLAYER_SIZE), pygame.SRCALPHA)
        if self.reversed_body_frame:
            self.body_frame = pygame.transform.flip(self.body_frame, True, False)

        self.frame.blit(self.body_frame, (0, self.PLAYER_SIZE*0.25))
        if self.reversed_head_frame:
            self.head_frame = pygame.transform.flip(self.head_frame, True, False)
        
        self.frame.blit(self.head_frame, ((self.PLAYER_SIZE - self.head_frame.get_width())//2, -3))
        self.image = self.frame
    
    def set_body_frame(self):
        if self.player.direction == Directions.LEFT or self.player.direction == Directions.RIGHT:
            self.x_legs_frame += 10
            if self.player.direction == Directions.LEFT: 
                self.reversed_body_frame = True
     
        self.body_frame = self.body_images[self.x_legs_frame]
        self.x_legs_frame %= 10
    
    def set_head_frame(self):
        x = self.x_head_frame
        self.reversed_head_frame = False
        if self.player.facing == Directions.LEFT or self.player.facing == Directions.RIGHT:
            x += 2
            if self.player.facing == Directions.LEFT:
                self.reversed_head_frame = True
        elif self.player.facing == Directions.UP:
            x += 4
        
        self.head_frame = self.head_images[x]
        self.head_frame = pygame.transform.scale(self.head_frame, (self.PLAYER_SIZE*0.9, self.PLAYER_SIZE*0.9))
    
    def play_death_animation(self):
        center_x = self.player.rect.centerx
        center_y = self.player.rect.centery
        self.death_time_left -= 1
        if self.death_time_left <= 0:
            if self.death_index > self.last_death_index:
                self.player.end_of_death_animation = True
                return
            
            frame_name = "die" + str(self.death_index)
            self.player.image = self.game.image_loader.player_animations_list[self.player_type.get_index()][frame_name]
            self.player.rect.width = self.player.image.get_width()
            self.player.rect.height = self.player.image.get_height()
            self.player.rect.centerx = center_x
            self.player.rect.centery = center_y

            self.death_time_left = self.death_frame_cd
            self.death_index += 1

    def get_init_mask(self):
        self.animate()
        mask = pygame.mask.from_surface(self.image)
        self.correct_player_mask(mask)
        return mask

    def correct_player_mask(self, mask):
        removed_hitbox_from_sides = pygame.Surface((mask.get_size()[0] * 0.25, mask.get_size()[1]))
        removed_hitbox_from_top = pygame.Surface((mask.get_size()[0], mask.get_size()[1] * 0.25))
        cut_mask_sides = pygame.mask.from_surface(removed_hitbox_from_sides)
        cut_mask_top = pygame.mask.from_surface(removed_hitbox_from_top)

        mask.erase(cut_mask_sides, (0, 0))
        mask.erase(cut_mask_sides, (mask.get_size()[0] - cut_mask_sides.get_size()[0], 0))
        mask.erase(cut_mask_top, (0, 0))