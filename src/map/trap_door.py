import pygame

from config import BLOCK_LAYER


class TrapDoor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * game.settings.TILE_SIZE - game.settings.TILE_SIZE / 2
        self.y = y * game.settings.TILE_SIZE
        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE

        self.image = game.image_loader.trap_door["closed"]
        self.help_control_image = game.image_loader.trap_door["help_control"]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.opened = False
        self.timer = 0
        self.animated = False

    def update(self):
        player_pos = pygame.Vector2(
            self.game.player.rect.centerx,
            self.game.player.rect.centery + self.game.settings.TILE_SIZE / 3,
        )
        trap_door_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        distance = player_pos.distance_to(trap_door_pos)

        if not self.animated and self.opened:
            self.timer -= 1
            if self.timer <= 0:
                self.image = self.game.image_loader.trap_door["opened"]
                self.opened = True
                self.animated = True
                self.game.sound_manager.play_if_not_playing("doorOpen")

        if distance <= self.game.settings.TILE_SIZE / 2 and self.animated:
            if self.game.map.level == 7:
                self.game.game_over_playing = True
            else:
                self.game.render_new_map()
                self.game.sound_manager.play("level_change")

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.opened:
            size = int(self.game.settings.TILE_SIZE * 1.1)
            help_width = self.help_control_image.get_width()
            screen.blit(self.help_control_image, (self.rect.centerx - help_width // 2, self.rect.y + size))


    def open(self):
        if self.opened:
            return

        self.opened = True
        self.timer = 120
