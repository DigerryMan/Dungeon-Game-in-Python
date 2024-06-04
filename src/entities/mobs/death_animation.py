import pygame


class DeathAnimator:
    def __init__(self, enemy, game):
        self.enemy = enemy
        self.game = game

        self.curr_frame = 0
        self.next_frame_time = 4
        self.dead_animation_time = 11 * self.next_frame_time
        self.dead_animation_time_left = self.dead_animation_time

        self.img = game.image_loader.others["death_animation"]
        self.death_images = []
        self.prepare_death_images()

    def prepare_death_images(self):
        death_mob_size = self.enemy.MOB_SIZE
        for x in range(12):
            image_help = self.img.subsurface(pygame.Rect(x * 32, 0, 32, 32))
            self.death_images.append(
                pygame.transform.scale(image_help, (death_mob_size, death_mob_size))
            )

    def death_animation(self):
        if self.dead_animation_time_left == self.dead_animation_time:
            centerx, centery = self.enemy.rect.centerx, self.enemy.rect.centery
            self.enemy.rect = self.death_images[self.curr_frame].get_rect()
            self.enemy.image = self.death_images[self.curr_frame]
            self.enemy.rect.centerx, self.enemy.rect.centery = centerx, centery

        self.dead_animation_time_left -= 1
        if self.dead_animation_time_left < 0:
            self.enemy.final_death()
        elif self.dead_animation_time_left % self.next_frame_time == 0:
            self.curr_frame += 1
            self.enemy.image = self.death_images[self.curr_frame]

    def prepare_death_images_for_fly(self):
        self.death_images.clear()
        death_mob_size = self.enemy.MOB_SIZE * 2
        for y in range(1, 4):
            for x in range(4):
                image_help = self.enemy.img.subsurface(
                    pygame.Rect(
                        x * death_mob_size,
                        y * death_mob_size,
                        death_mob_size,
                        death_mob_size,
                    )
                )
                self.death_images.append(
                    pygame.transform.scale(
                        image_help, (self.enemy.MOB_SIZE, self.enemy.MOB_SIZE)
                    )
                )

    def fly_death_animation(self):
        if self.dead_animation_time_left == self.dead_animation_time:
            self.enemy.curr_frame = 0
            self.enemy.image = self.death_images[self.enemy.curr_frame]

        self.dead_animation_time_left -= 1
        if self.dead_animation_time_left < 0:
            self.enemy.final_death()
        elif self.dead_animation_time_left % self.next_frame_time == 0:
            self.enemy.curr_frame += 1
            self.enemy.image = self.death_images[self.enemy.curr_frame]

    def scale_to_new_size(self, size):
        for index, image in enumerate(self.death_images):
            self.death_images[index] = pygame.transform.scale(image, (size, size))

    def scale_to_new_size_v2(self, width, height):
        for index, image in enumerate(self.death_images):
            self.death_images[index] = pygame.transform.scale(image, (width, height))
