import pygame

from entities.mobs.boss.shaking_animation import ShakingAnimation

class DukeAnimation():
    def __init__(self, boss, game):
        self.boss = boss
        self.game = game
        self.img = game.image_loader.bosses["duke"]
        self.images = []
        self.prepare_images()
        self.boss.image = self.images[2]
        self.boss.unchanged_image = self.boss.image.copy()
        self.boss.mask = pygame.mask.from_surface(self.boss.image)

        self.intro_image = None
        self.intro_name = None
        self.prepare_intro_images()

        self.time = 20
        self.time_cd = 20
        self.frame_index = 0

        #SHAKING
        self.shaking_animation = ShakingAnimation(boss)

        # SPAWNING MOBS
        self.spawn_frames = [0, 3, 0, 2]
        self.spawn_times_of_frames = [int(0.75 * self.boss.spawning_time_cd), int(0.5 * self.boss.spawning_time_cd), int(0.38 * self.boss.spawning_time_cd), 2]
        self.spawn_index = 0 

    def prepare_intro_images(self):
        img = self.img.subsurface(pygame.Rect(22, 175, 144, 180))
        self.intro_image = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))
        img = self.img.subsurface(pygame.Rect(195, 187, 151, 46))
        self.intro_name = pygame.transform.scale(img, (img.get_width() * 3 * self.game.settings.SCALE, img.get_height() * 3 * self.game.settings.SCALE))

    def prepare_images(self):
        for y in range(2):
            for x in range(2):
                image = self.img.subsurface(pygame.Rect(x * 80, y * 64, 80, 64))
                self.images.append(pygame.transform.scale(image, (self.boss.MOB_SIZE, self.boss.MOB_SIZE)))

    def animate(self):
        self.shaking_animation.shaking_animation_x()
        self.shaking_animation.shaking_animation_y()
        if self.boss.is_spawning_mobs:
            self.enemies_spawning_animation()
        
    def enemies_spawning_animation(self):
        if self.boss.spawning_time in self.spawn_times_of_frames:
            self.boss.image = self.images[self.spawn_frames[self.spawn_index]]
            self.boss.is_change_of_frame = True
            self.boss.unchanged_image = self.boss.image.copy()
            self.spawn_index += 1
            self.spawn_index %= 4
        
    def change_opacity(self, image, opacity=50):
        image = image.copy()
        if 0 <= opacity <= 255:
            for x in range(image.get_width()):
                for y in range(image.get_height()):
                    r, g, b, a = image.get_at((x, y))
                    if a != 0:
                        image.set_at((x, y), (r, g, b, opacity))
        return image