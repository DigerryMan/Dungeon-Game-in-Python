import pygame


class BossHealthBar:
    def __init__(self, game, boss):
        self.game = game
        self.boss = boss
        self.full_bar_image = game.image_loader.get_stat_bar_image("boss_full_bar")
        self.empty_bar_image = game.image_loader.get_stat_bar_image("boss_empty_bar")
        self.resize_images()

        self.width = self.full_bar_image.get_width()
        self.height = self.full_bar_image.get_height()
        self.bar_x = (self.game.settings.WIN_WIDTH - self.width) // 2
        self.bar_y = self.game.settings.TILE_SIZE // 2

    def resize_images(self):
        new_width = self.game.settings.WIN_WIDTH // 3
        factor = new_width / self.full_bar_image.get_width()
        new_height = int(self.full_bar_image.get_height() * factor)
        new_size = (
            new_width * self.game.settings.SCALE,
            new_height * self.game.settings.SCALE,
        )

        self.full_bar_image = pygame.transform.scale(self.full_bar_image, new_size)
        self.empty_bar_image = pygame.transform.scale(self.empty_bar_image, new_size)

    def draw(self, screen):
        curr_width = self.boss._health / self.boss._max_health * self.width

        screen.blit(self.empty_bar_image, (self.bar_x, self.bar_y))
        screen.blit(
            self.full_bar_image,
            (self.bar_x, self.bar_y),
            (0, 0, curr_width, self.height),
        )
