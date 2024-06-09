import pygame

from config import FPS


class LevelLoadingScreen:
    def __init__(self, menu):
        self.menu = menu
        self.game = menu.game
        self.duration = 8000
        self.fade_duration = 2000

    def display(self):
        self.game.sound_manager.stop_all_with_fadeout(250)

        current_level = self.game.current_level - 1

        background = self.game.image_loader.images_dict["level_loading_background"]

        spotlight_size = (
            self.game.image_loader.images_dict["spotlight"].get_width() * 2,
            self.game.image_loader.images_dict["spotlight"].get_height() * 2,
        )
        spotlight = pygame.transform.scale(
            self.game.image_loader.images_dict["spotlight"], spotlight_size
        )
        spotlight_positon = (
            self.game.settings.WIN_WIDTH // 2 - spotlight.get_width() // 2,
            -spotlight.get_height() // 1.7,
        )

        level_icons = [self.game.image_loader.minis[f"{i}"] for i in range(1, 8)]
        offset = level_icons[0].get_width() * 1.2
        mid_pos = self.game.settings.WIN_WIDTH // 2 - level_icons[0].get_width() // 2.45
        level_icons_positions = [
            (mid_pos + offset * i, offset // 2) for i in range(-3, 4)
        ]

        corridor = self.game.image_loader.minis["corridor"]
        corridor_positions = [
            (mid_pos + offset * i - offset // 2, offset // 1.5) for i in range(-2, 4)
        ]

        player_icon = self.game.image_loader.minis["player"]
        player_icon_position = (
            level_icons_positions[current_level - 1][0]
            + level_icons[0].get_width() // 2
            - player_icon.get_width() // 2,
            level_icons_positions[current_level - 1][1]
            + level_icons[0].get_height() // 2
            - player_icon.get_height() // 1.5,
        )

        player_spot_size = (
            self.game.image_loader.boss_intro["playerspot"].get_width() * 1.4,
            self.game.image_loader.boss_intro["playerspot"].get_height() * 1.4,
        )
        player_spot = pygame.transform.scale(
            self.game.image_loader.boss_intro["playerspot"], player_spot_size
        )
        player_spot_position = (
            self.game.settings.WIN_WIDTH // 2 - player_spot.get_width() // 2,
            self.game.settings.WIN_HEIGHT // 1.4,
        )

        jump_start = 2000
        jump_end = 6000
        jump_duration = jump_end - jump_start
        jump_offset = 0

        boss_icon = self.game.image_loader.minis["final_boss"]
        boss_icon_position = (
            level_icons_positions[6][0]
            + level_icons[0].get_width() // 2
            - player_icon.get_width() // 1.8,
            level_icons_positions[6][1]
            + level_icons[0].get_height() // 2
            - player_icon.get_height() // 2,
        )

        player_image = self.game.player.animation.intro_image
        player_image_position = (
            self.game.settings.WIN_WIDTH // 2 - player_image.get_width() // 2,
            self.game.settings.WIN_HEIGHT // 1.5,
        )

        should_display = True
        start_time = pygame.time.get_ticks()

        self.game.sound_manager.play_with_fadein("level_change", 500)

        while should_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    should_display = False

            elapsed_time = pygame.time.get_ticks() - start_time

            if elapsed_time >= self.duration:
                should_display = False
                self.game.sound_manager.play_with_fadein(
                    "basementLoop", 2000, looped=True
                )
                break

            self.game.screen.blit(background, (0, 0))
            self.game.screen.blit(player_spot, player_spot_position)
            self.game.screen.blit(player_image, player_image_position)
            self.game.screen.blit(spotlight, spotlight_positon)

            for corrid in corridor_positions:
                self.game.screen.blit(corridor, corrid)
            for icon, position in zip(level_icons, level_icons_positions):
                self.game.screen.blit(icon, position)

            if jump_start < elapsed_time < jump_end:
                jump_progress = (elapsed_time - jump_start) / jump_duration
                jump_offset = offset * jump_progress

            player_icon_position = (
                level_icons_positions[current_level - 1][0]
                + level_icons[0].get_width() // 2
                - player_icon.get_width() // 2
                + jump_offset,
                level_icons_positions[current_level - 1][1]
                + level_icons[0].get_height() // 2
                - player_icon.get_height() // 1.5,
            )

            self.game.screen.blit(player_icon, player_icon_position)
            self.game.screen.blit(boss_icon, boss_icon_position)

            if elapsed_time < self.duration:
                if elapsed_time < self.fade_duration:  # Fade in
                    alpha = (255 * elapsed_time) // self.fade_duration
                elif elapsed_time > self.duration - self.fade_duration:  # Fade out
                    remaining_time = self.duration - elapsed_time
                    alpha = (255 * remaining_time) // self.fade_duration
                else:  # No fade
                    alpha = 255

                fade_surface = pygame.Surface(
                    (self.game.settings.WIN_WIDTH, self.game.settings.WIN_HEIGHT)
                )
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(255 - alpha)
                self.game.screen.blit(fade_surface, (0, 0))

            self.game.clock.tick(FPS)
            pygame.display.update()
