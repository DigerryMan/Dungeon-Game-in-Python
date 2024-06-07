import pygame

from config import FPS


class AudioSettingsScreen:
    def __init__(self, main_settings):
        self.main_settings = main_settings
        self.menu = main_settings.menu
        self.game = main_settings.game

        self.current_music_volume = 2
        self.current_gameplay_volume = 5

    def display(self):
        arrow_positions = [
            (
                self.game.settings.WIN_WIDTH // 2.61,
                self.game.settings.WIN_HEIGHT // 2.73,
            ),
            (
                self.game.settings.WIN_WIDTH // 2.58,
                self.game.settings.WIN_HEIGHT // 2.15,
            ),
        ]

        current_arrow = 0

        dislpay_sound_settings_playing = True

        music_ticks = [
            self.game.image_loader.images_dict["tick_transparent"].copy()
            for _ in range(11)
        ]
        gameplay_ticks = [
            self.game.image_loader.images_dict["tick_transparent"].copy()
            for _ in range(11)
        ]

        for i in range(int(self.current_music_volume) + 1):
            music_ticks[i] = self.game.image_loader.images_dict["tick"].copy()

        for i in range(int(self.current_gameplay_volume) + 1):
            gameplay_ticks[i] = self.game.image_loader.images_dict["tick"].copy()

        def draw_ticks():
            for i in range(1, 11):
                self.game.screen.blit(
                    music_ticks[i],
                    (
                        self.game.settings.WIN_WIDTH // 2
                        + i * music_ticks[i].get_width() * 0.7,
                        self.game.settings.WIN_HEIGHT // 2.8
                        - i * music_ticks[i].get_height() * 0.045,
                    ),
                )
                self.game.screen.blit(
                    gameplay_ticks[i],
                    (
                        self.game.settings.WIN_WIDTH // 1.95
                        + i * gameplay_ticks[i].get_width() * 0.7,
                        self.game.settings.WIN_HEIGHT // 2.2
                        - i * gameplay_ticks[i].get_height() * 0.045,
                    ),
                )

        while dislpay_sound_settings_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dislpay_sound_settings_playing = False
                    self.main_settings.settings_playing = False
                    self.game.menu_playing = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.game.sound_manager.play("selectLeft")
                        current_arrow = current_arrow + 1 if current_arrow < 1 else 0

                    if event.key == pygame.K_UP:
                        self.game.sound_manager.play("selectRight")
                        current_arrow = current_arrow - 1 if current_arrow > 0 else 1

                    if event.key == pygame.K_LEFT:
                        if current_arrow == 0:
                            if self.current_music_volume > 0:
                                self.game.sound_manager.play("selectLeft")
                                music_ticks[self.current_music_volume] = (
                                    self.game.image_loader.images_dict[
                                        "tick_transparent"
                                    ].copy()
                                )
                                self.current_music_volume = (
                                    self.current_music_volume - 1
                                )
                                self.game.sound_manager.set_music_volume(
                                    self.current_music_volume
                                )

                        elif current_arrow == 1:
                            if self.current_gameplay_volume > 0:
                                self.game.sound_manager.play("selectLeft")
                                gameplay_ticks[self.current_gameplay_volume] = (
                                    self.game.image_loader.images_dict[
                                        "tick_transparent"
                                    ].copy()
                                )
                                self.current_gameplay_volume = (
                                    self.current_gameplay_volume - 1
                                )
                                self.game.sound_manager.set_sound_volume(
                                    self.current_gameplay_volume
                                )

                    if event.key == pygame.K_RIGHT:
                        if current_arrow == 0:
                            if self.current_music_volume < 10:
                                self.game.sound_manager.play("selectRight")
                                self.current_music_volume = (
                                    self.current_music_volume + 1
                                )
                                music_ticks[self.current_music_volume] = (
                                    self.game.image_loader.images_dict["tick"].copy()
                                )
                                self.game.sound_manager.set_music_volume(
                                    self.current_music_volume
                                )

                        elif current_arrow == 1:
                            if self.current_gameplay_volume < 10:
                                self.game.sound_manager.play("selectRight")
                                self.current_gameplay_volume = (
                                    self.current_gameplay_volume + 1
                                )
                                gameplay_ticks[self.current_gameplay_volume] = (
                                    self.game.image_loader.images_dict["tick"].copy()
                                )
                                self.game.sound_manager.set_sound_volume(
                                    self.current_gameplay_volume
                                )

                    if event.key == pygame.K_ESCAPE:
                        self.game.sound_manager.play("pageTurn")
                        dislpay_sound_settings_playing = False

            self.game.screen.blit(self.menu.sound_settings_card, (0, 0))
            self.game.screen.blit(self.menu.menu_background, (0, 0))
            self.menu.display_tilted_main_title()

            self.game.screen.blit(
                self.menu.arrow,
                (arrow_positions[current_arrow][0], arrow_positions[current_arrow][1]),
            )

            draw_ticks()

            self.game.clock.tick(FPS)
            pygame.display.update()
