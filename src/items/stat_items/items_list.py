import random

import pygame

from config import DROP_LOOT_EVERYTIME
from items.stat_items.categories import Categories


class ItemsList:
    def __init__(self, game):
        self.game = game

        self.very_commons = {}
        self.commons = {}
        self.epics = {}
        self.legendaries = {}

        # PILLS

        self.very_commons["health_pill"] = {
            "name": "Health pill",
            "category": Categories.VERY_COMMON,
            "stats": {"health": [-1, 1]},
            "image": game.image_loader.lootables["health_pill"],
        }

        self.very_commons["dmg_pill"] = {
            "name": "Damage pill",
            "category": Categories.VERY_COMMON,
            "stats": {"dmg": [-0.2, -0.1, 0.1, 0.2]},
            "image": game.image_loader.lootables["dmg_pill"],
        }

        self.very_commons["dmg_reduction_pill"] = {
            "name": "Damage reduction pill",
            "category": Categories.VERY_COMMON,
            "stats": {"dmg_reduction": [-0.04, -0.02, 0.02, 0.04]},
            "image": game.image_loader.lootables["dmg_reduction_pill"],
        }

        self.very_commons["shooting_cooldown_pill"] = {
            "name": "Shooting cooldown pill",
            "category": Categories.VERY_COMMON,
            "stats": {"shooting_cooldown": [0.04, 0.08, -0.08, -0.04]},
            "image": game.image_loader.lootables["shooting_cooldown_pill"],
        }

        self.very_commons["shot_speed_pill"] = {
            "name": "Shot speed pill",
            "category": Categories.VERY_COMMON,
            "stats": {"shot_speed": [-1, -0.5, 0.5, 1]},
            "image": game.image_loader.lootables["shot_speed_pill"],
        }

        self.very_commons["bullet_fly_time_pill"] = {
            "name": "Bullet fly time pill",
            "category": Categories.VERY_COMMON,
            "stats": {"bullet_fly_time": [-0.05, 0.05]},
            "image": game.image_loader.lootables["bullet_fly_time_pill"],
        }

        self.very_commons["speed_pill"] = {
            "name": "Speed pill",
            "category": Categories.VERY_COMMON,
            "stats": {"speed": [-1, 1]},
            "image": game.image_loader.lootables["speed_pill"],
        }

        self.very_commons["luck_pill"] = {
            "name": "Luck pill",
            "category": Categories.VERY_COMMON,
            "stats": {"luck": [-0.05, -0.025, 0.025, 0.05]},
            "image": game.image_loader.lootables["luck_pill"],
        }

        self.very_commons["immortality_pill"] = {
            "name": "Immortality pill",
            "category": Categories.VERY_COMMON,
            "stats": {"immortality": [-0.25, -0.125, 0.125, 0.25]},
            "image": game.image_loader.lootables["immortality_pill"],
        }

        # COMMON ITEMS

        self.commons["heart"] = {
            "name": "Heart",
            "category": Categories.COMMON,
            "stats": {"health": 1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(3 * 32, 2 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["armor"] = {
            "name": "Armor",
            "category": Categories.COMMON,
            "stats": {"dmg_reduction": 0.1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(3 * 32, 21 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["small_sword"] = {
            "name": "Small sword",
            "category": Categories.COMMON,
            "stats": {"dmg": 0.2},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(15 * 32, 19 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["glasses"] = {
            "name": "Glasses",
            "category": Categories.COMMON,
            "stats": {"bullet_fly_time": 0.2, 
                      "shooting_cooldown": 0.05},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(0 * 32, 12 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["green_syringe"] = {
            "name": "Green syringe",
            "category": Categories.COMMON,
            "stats": {"shot_speed": 2, 
                      "shooting_cooldown": 0.05},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(13 * 32, 0 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["red_pepper"] = {
            "name": "Red pepper",
            "category": Categories.COMMON,
            "stats": {"speed": 2},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(22 * 32, 9 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["pills"] = {
            "name": "Pills",
            "category": Categories.COMMON,
            "stats": {"speed": 1, "immortality": 0.1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(18 * 32, 4 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["paw"] = {
            "name": "Paw",
            "category": Categories.COMMON,
            "stats": {"health": 1, "bullet_fly_time": 0.1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(9 * 32, 6 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["suspicous_juice"] = {
            "name": "Suspicious juice",
            "category": Categories.COMMON,
            "stats": {"speed": -1, "dmg": 0.25, "shooting_cooldown": 0.05, "health": 1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(13 * 32, 9 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["gameboy"] = {
            "name": "Gameboy",
            "category": Categories.COMMON,
            "stats": {"dmg": 0.1, "shooting_cooldown": 0.05},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(9 * 32, 4 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["peanut_butter"] = {
            "name": "Peanut butter",
            "category": Categories.COMMON,
            "stats": {"health": 1, "dmg": 0.1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(17 * 32, 10 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.commons["explorers_guide"] = {
            "name": "Explorer's guide",
            "category": Categories.COMMON,
            "stats": {"speed": 1, "health": 1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(19 * 32, 5 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        # EPIC ITEMS

        self.epics["angel"] = {
            "name": "Angel",
            "category": Categories.EPIC,
            "stats": {"immortality": 0.5},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(5 * 32, 19 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.epics["big_sword"] = {
            "name": "Big sword",
            "category": Categories.EPIC,
            "stats": {"dmg": 0.5},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(26 * 32, 13 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.epics["holy_cross"] = {
            "name": "Holy cross",
            "category": Categories.EPIC,
            "stats": {"luck": 0.1, "speed": 1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(36 * 32, 6 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.epics["glass_cannon"] = {
            "name": "Glass cannon",
            "category": Categories.EPIC,
            "stats": {
                "description": "You deal twice the damage, but take twice the damage!",
                "dmg_multiplier": 2,
                "dmg_taken_multiplier": 2,
            },
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(7 * 32, 17 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.epics["darkhold"] = {
            "name": "Darkhold",
            "category": Categories.EPIC,
            "stats": {"dmg": 1, "health": -1},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(7 * 32, 14 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.epics["holy_bullet"] = {
            "name": "Holy bullet",
            "category": Categories.EPIC,
            "stats": {"dmg": 0.5, "immortality": 0.1, "shooting_cooldown": 0.05},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(9 * 32, 18 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        # LEGENDARY ITEMS

        self.legendaries["PHD"] = {
            "name": "PHD",
            "category": Categories.LEGENDARY,
            "stats": {
                "description": "You are immune to negative effects of the pills",
                "PHD_obtained": 1,
            },
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(0 * 32, 0 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.legendaries["friendly_ghost"] = {
            "name": "Friendly ghost",
            "category": Categories.LEGENDARY,
            "stats": {
                "description": "A friendly ghost is there to assist you",
                "friendly_ghost": 1,
            },
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(8 * 32, 5 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE // 2, game.settings.TILE_SIZE // 2),
            ),
        }

        self.legendaries["eye_of_horus"] = {
            "name": "Eye of Horus",
            "category": Categories.LEGENDARY,
            "stats": {
                "health": 2,
                "dmg": 1,
                "dmg_reduction": 0.2,
                "shot_speed": 2,
                "bullet_fly_time": 0.5,
                "luck": 0.1,
                "immortality": 0.5,
                "shooting_cooldown": 0.1,
                "speed": 1,
            },
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(33 * 32, 8 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

        self.legendaries["bulls_eye"] = {
            "name": "Bull's eye",
            "category": Categories.LEGENDARY,
            "stats": {"description": "Double shot", "extra_shot_time": 5},
            "image": pygame.transform.scale(
                game.image_loader.get_image("items").subsurface(
                    pygame.Rect(5 * 32, 8 * 32, 32, 32)
                ),
                (game.settings.TILE_SIZE, game.settings.TILE_SIZE),
            ),
        }

    def get_random_item(self, category):
        if DROP_LOOT_EVERYTIME:  # FOR TESTING PURPOSES!
            return self.legendaries["friendly_ghost"]
        else:
            if category == Categories.VERY_COMMON:
                return random.choice(list(self.very_commons.values()))

            elif category == Categories.COMMON:
                return random.choice(list(self.commons.values()))

            elif category == Categories.EPIC:
                return random.choice(list(self.epics.values()))

            elif category == Categories.LEGENDARY:
                return random.choice(list(self.legendaries.values()))

        return None

    def get_boss_item(self, boss):
        match boss:
            case "monstro":
                return self.legendaries["PHD"]
            case "husk":
                return self.legendaries["friendly_ghost"]
            case "satan":
                return self.legendaries["eye_of_horus"]
            case "forsaken":
                return self.legendaries["bulls_eye"]
            case _:
                return None
