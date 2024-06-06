import random

from entities.enemy import Enemy
from entities.player.player import Player


class RoomDrawer:
    def __init__(self, room):
        self.game = room.game
        self.room = room
        self.room_type = room.room_type
        self.level = room.level
        self.room_graphics = {}

        self.select_graphics()

    def select_graphics(self):
        if self.room_type == "start" and self.level == 1:
            self.room_graphics["controls"] = self.game.image_loader.get_image(
                "controls"
            )

        match self.level:
            case 1:
                self.room_graphics["background_image"] = (
                    self.game.image_loader.get_image(
                        "basement" + str(random.randint(1, 4))
                    )
                )
            case 2:
                self.room_graphics["background_image"] = (
                    self.game.image_loader.get_image("cave" + str(random.randint(1, 5)))
                )
            case 3:
                self.room_graphics["background_image"] = (
                    self.game.image_loader.get_image(
                        "catacombs" + str(random.randint(1, 3))
                    )
                )
            case 4:
                self.room_graphics["background_image"] = (
                    self.game.image_loader.get_image("necropolis1")
                )
            case 5:
                self.room_graphics["background_image"] = (
                    self.game.image_loader.get_image(
                        "depths" + str(random.randint(1, 3))
                    )
                )
            case 6:
                self.room_graphics["background_image"] = (
                    self.game.image_loader.get_image(
                        "bluewomb" + str(random.randint(1, 3))
                    )
                )
            case 7:
                self.room_graphics["background_image"] = (
                    self.game.image_loader.get_image("womb" + str(random.randint(1, 4)))
                )

        if self.room_type == "shop":
            self.room_graphics["background_image"] = self.game.image_loader.get_image(
                "shop_room"
            )

        self.room_graphics["shading"] = self.game.image_loader.get_image("shading")

    def draw(self, screen):
        screen.blit(
            self.room_graphics["background_image"],
            (
                -self.game.settings.WIN_WIDTH * 0.04,
                -self.game.settings.WIN_HEIGHT * 0.04,
            ),
        )
        if self.room_type == "start" and self.level == 1:
            controls_rect = self.room_graphics["controls"].get_rect()
            screen.blit(
                self.room_graphics["controls"],
                (
                    (self.game.settings.WIN_WIDTH - controls_rect.width) // 2.1,
                    (self.game.settings.WIN_HEIGHT - controls_rect.height) // 2,
                ),
            )

        self.game.doors.draw(screen)
        self.game.blocks.draw(screen)
        self.game.items.draw(screen)
        for trapdoor in self.game.trap_door.sprites():
            trapdoor.draw(screen)
        self.game.destroyed_blocks.draw(screen)

        for shop_stand in self.room.shop_stands:
            shop_stand.draw()

        to_be_sorted = (
            self.game.entities.sprites()
            + self.game.items.sprites()
            + self.game.chest.sprites()
        )

        sprite_list = sorted(to_be_sorted, key=lambda sprite: sprite._layer)
        for sprite in sprite_list:
            if isinstance(sprite, Enemy):
                sprite.draw_additional_images(screen)
            screen.blit(sprite.image, sprite.rect)
            if isinstance(sprite, Player):
                sprite.draw_additional_images(screen)

        screen.blit(
            self.room_graphics["shading"],
            (
                -self.game.settings.WIN_WIDTH * 0.04,
                -self.game.settings.WIN_HEIGHT * 0.04,
            ),
        )
