import pygame

from entities.mobs.boss.shaking_animation import ShakingAnimation


class SatanAnimiation:
    waking_up_frames = [21, 22, 23, 1]
    hands_frames = [1, 13, 14, 15, 1]
    laser_frames = [7, 3, 7, 9, 10, 7, 1, 0]
    mouth_frames = [1, 2, 6, 8, 0, 1]
    flying_frames = [1, 25]

    def __init__(self, boss, game, _skin: str = "satan"):
        self.boss = boss
        self.game = game

        self.img = game.image_loader.bosses[_skin]
        self.img_red =  game.image_loader.bosses[_skin+"_hit"]
        self.images = []
        self.images_red = []
        self.frame_index = 0
        self.prepare_images()

        
        self.img_hit = game.image_loader.bosses[_skin+"_hit"]
        self.images_hit = []
        self.prepare_hit_images()

        self.boss.image = self.images[21]
        self.boss.unchanged_image = self.images_red[21]
        self.boss.mask = pygame.mask.from_surface(self.boss.image)

        self.intro_image = None
        self.intro_name = None
        self.prepare_intro_images(_skin)

        self.time = self.time_cd = 10
        self.index = 0

        # SHAKING
        self.shaking_animation = ShakingAnimation(boss)

        # TIME STAGES OF FRAMES
        self.waking_up_time_stages = [0.99, 0.2, 0.12, 0.06]
        self.waking_up_time_stages = [
            int(time * self.boss.bullets_from_hands_period)
            for time in self.waking_up_time_stages
        ]
        self.hands_time_stages = [0.99, 0.8, 0.49, 0.4, 0.12]
        self.hands_time_stages = [
            int(time * self.boss.bullets_from_hands_period)
            for time in self.hands_time_stages
        ]
        self.laser_time_stages = [0.99, 0.95, 0.87, 0.75, 0.42, 0.3, 0.2, 0.1]
        self.laser_time_stages = [
            int(time * self.boss.laser_breath_period) for time in self.laser_time_stages
        ]
        self.mouth_time_stages = [0.99, 0.92, 0.83, 0.55, 0.25, 0.05]
        self.mouth_time_stages = [
            int(time * self.boss.mouth_attack_period) for time in self.mouth_time_stages
        ]
        self.flying_time_stages = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]
        self.flying_time_stages = [
            int(time * self.boss.flying_period) for time in self.flying_time_stages
        ]

    def prepare_intro_images(self, _skin: str = "satan"):
        if _skin == "satan":
            img = self.img.subsurface(pygame.Rect(30, 752, 159, 163))
            self.intro_image = pygame.transform.scale(
                img,
                (
                    img.get_width() * 3 * self.game.settings.SCALE,
                    img.get_height() * 3 * self.game.settings.SCALE,
                ),
            )
            img = self.img.subsurface(pygame.Rect(237, 805, 122, 38))
            self.intro_name = pygame.transform.scale(
                img,
                (
                    img.get_width() * 3 * self.game.settings.SCALE,
                    img.get_height() * 3 * self.game.settings.SCALE,
                ),
            )
        else:
            img = self.img.subsurface(pygame.Rect(30, 752, 159, 163))
            self.intro_image = pygame.transform.scale(
                img,
                (
                    img.get_width() * 3 * self.game.settings.SCALE,
                    img.get_height() * 3 * self.game.settings.SCALE,
                ),
            )
            img = self.img.subsurface(pygame.Rect(237, 805, 170, 38))
            self.intro_name = pygame.transform.scale(
                img,
                (
                    img.get_width() * 3 * self.game.settings.SCALE,
                    img.get_height() * 3 * self.game.settings.SCALE,
                ),
            )

    def prepare_images(self):
        size = self.boss.MOB_WIDTH, self.boss.MOB_HEIGHT
        for y in range(6):
            for x in range(4):
                image = self.img.subsurface(pygame.Rect(x * 200, y * 120, 200, 120))
                self.images.append(pygame.transform.scale(image, size))

                image_red = self.img_red.subsurface(pygame.Rect(x * 200, y * 120, 200, 120))
                self.images_red.append(pygame.transform.scale(image_red, size))

        image = self.img.subsurface(pygame.Rect(4 * 200, 2 * 120, 200, 120))
        self.images.append(pygame.transform.scale(image, size))

        image = self.img.subsurface(pygame.Rect(4 * 200, 3 * 120, 200, 120))
        self.images.append(pygame.transform.scale(image, size))

        image = self.img.subsurface(pygame.Rect(4 * 200, 0, 200, 240))
        self.images.append(pygame.transform.scale(image, size))
    
    def prepare_hit_images(self):
        size = self.boss.MOB_WIDTH, self.boss.MOB_HEIGHT
        for y in range(6):
            for x in range(4):
                image = self.img_hit.subsurface(pygame.Rect(x * 200, y * 120, 200, 120))
                self.images_hit.append(pygame.transform.scale(image, size))

        image = self.img_hit.subsurface(pygame.Rect(4 * 200, 2 * 120, 200, 120))
        self.images_hit.append(pygame.transform.scale(image, size))

        image = self.img_hit.subsurface(pygame.Rect(4 * 200, 3 * 120, 200, 120))
        self.images_hit.append(pygame.transform.scale(image, size))

        image = self.img_hit.subsurface(pygame.Rect(4 * 200, 0, 200, 240))
        self.images_hit.append(pygame.transform.scale(image, size))

    def animate(self):
        if self.boss.boss_figth_start_active:
            self.waking_up_animation()
        elif self.boss.bullets_from_hands_active:
            self.shaking_animation.shake_animation_x_and_y()
            self.animate_bullets_from_hands()
        elif self.boss.laser_breath_active:
            self.shaking_animation.shaking_animation_x(True)
            self.animate_laser_breath()
        elif self.boss.mouth_attack_active:
            self.shaking_animation.shaking_animation_x()
            self.animate_mouth_attack()
        elif self.boss.flying_active:
            self.flying_animation()
            self.shaking_animation.shake_animation_x_and_y()

    def waking_up_animation(self):
        self.animate_full_time_stage(
            self.boss.start_time,
            self.waking_up_time_stages,
            SatanAnimiation.waking_up_frames,
            self.waking_up_time_stages,
        )

    def animate_bullets_from_hands(self):
        self.animate_full_time_stage(
            self.boss.bullets_from_hands_time,
            self.hands_time_stages,
            SatanAnimiation.hands_frames,
            self.hands_time_stages,
        )

    def animate_laser_breath(self):
        self.animate_full_time_stage(
            self.boss.laser_breath_time,
            self.laser_time_stages,
            SatanAnimiation.laser_frames,
            self.laser_time_stages,
        )

    def animate_mouth_attack(self):
        self.animate_full_time_stage(
            self.boss.mouth_attack_time,
            self.mouth_time_stages,
            SatanAnimiation.mouth_frames,
            self.mouth_time_stages,
        )

    def flying_animation(self):
        self.animate_full_time_stage(
            self.boss.flying_time,
            self.flying_time_stages,
            SatanAnimiation.flying_frames,
            SatanAnimiation.flying_frames,
        )

    def animate_full_time_stage(self, boss_condition, time_stage, frames, modulo_cond):
        if boss_condition in time_stage:
            self.boss.image = self.images[frames[self.frame_index]]
            self.boss.original_image_copy = self.images[frames[self.frame_index]]
            self.boss.is_change_of_frame = True
            self.boss.unchanged_image = self.images_hit[frames[self.frame_index]]
            self.boss.mask = pygame.mask.from_surface(self.boss.image)
            self.frame_index += 1
            self.frame_index %= len(modulo_cond)
