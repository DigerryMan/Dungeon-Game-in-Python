from config import DROP_LOOT_EVERYTIME
from items.stat_items.categories import Categories
import pygame
import random

class ItemsList():
    def __init__(self, game):
        self.game = game

        self.very_commons = {}
        self.commons = {}
        self.epics = {}
        self.legendaries = {}

        self.very_commons["health_pill"] = {
            "name": "Health pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "health": [-1, -0.5, 0.5, 1]
            },
            "image": game.image_loader.lootables["health_pill"]
        }

        self.very_commons["dmg_pill"] = {
            "name": "Damage pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "dmg": [-0.2, -0.1, 0.1, 0.2]
            },
            "image": game.image_loader.lootables["dmg_pill"]
        }

        self.very_commons["dmg_reduction_pill"] = {
            "name": "Damage reduction pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "dmg_reduction": [-0.1, -0.05, 0.05, 0.1]
            },
            "image": game.image_loader.lootables["dmg_reduction_pill"]
        }

        self.very_commons["shooting_cooldown_pill"] = {
            "name": "Shooting cooldown pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "shooting_cooldown": [-0.8, -0.04, 0.04, 0.8]
            },
            "image": game.image_loader.lootables["shooting_cooldown_pill"]
        }

        self.very_commons["shot_speed_pill"] = {
            "name": "Shot speed pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "shot_speed": [-1, -0.5, 0.5, 1]
            },
            "image": game.image_loader.lootables["shot_speed_pill"]
        }

        self.very_commons["bullet_fly_time_pill"] = {
            "name": "Bullet fly time pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "bullet_fly_time": [-0.1, 0.1]
            },
            "image": game.image_loader.lootables["bullet_fly_time_pill"]
        }

        self.very_commons["speed_pill"] = {
            "name": "Speed pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "speed": [-0.5, -0.25, 0.25, 0.5]
            },
            "image": game.image_loader.lootables["speed_pill"]
        }

        self.very_commons["luck_pill"] = {
            "name": "Luck pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "luck": [-0.05, -0.025, 0.025, 0.05]
            },
            "image": game.image_loader.lootables["luck_pill"]
        }

        self.very_commons["immortality_pill"] = {
            "name": "Immortality pill",
            "category": Categories.VERY_COMMON,
            "stats": {
                "immortality": [-0.25, -0.125, 0.125, 0.25]
            },
            "image": game.image_loader.lootables["immortality_pill"]
        }

        self.commons["heart"] = {
            "name": "Heart",
            "category": Categories.COMMON,
            "stats": {
                "health": 1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(3 * 32, 2 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["armor"] = {
            "name": "Armor",
            "category": Categories.COMMON,
            "stats": {
                "dmg_reduction": 0.1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(3 * 32, 21 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["small_sword"] = {
            "name": "Small sword",
            "category": Categories.COMMON,
            "stats": {
                "dmg": 0.2
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(15 * 32, 19 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["glasses"] = {
            "name": "Glasses",
            "category": Categories.COMMON,
            "stats": {
                "bullet_fly_time": 0.2
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(12 * 32, 3 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.commons["green_syringe"] = {
            "name": "Green syringe",
            "category": Categories.COMMON,
            "stats": {
                "shot_speed": 2
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(13 * 32, 0 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }





        self.epics["angel"] = {
            "name": "Angel",
            "category": Categories.EPIC,
            "stats": {
                "immortality": 0.5
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(5 * 32, 19 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.epics["big_sword"] = {
            "name": "Big sword",
            "category": Categories.EPIC,
            "stats": {
                "dmg": 0.5
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(26 * 32, 13 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.epics["holy_cross"] = {
            "name": "Holy cross",
            "category": Categories.EPIC,
            "stats": {
                "luck": 0.1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(36 * 32, 6 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.epics["glass_cannon"] = {
            "name": "Glass cannon",
            "category": Categories.EPIC,
            "stats": {
                "description": "You deal twice the damage, but take twice the damage!",
                "dmg_multiplier": 2,
                "dmg_taken_multiplier": 2
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(7 * 32, 17 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.epics["PHD"] = {
            "name": "PHD",
            "category": Categories.EPIC,
            "stats":{
                "description": "You are immune to negative effects of the pills",
                "PHD_obtained": 1,
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(0 * 32, 0 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }

        self.legendaries["friendly_ghost"] = {
            "name": "Friendly ghost",
            "category": Categories.LEGENDARY,
            "stats": {
                "description": "A friendly ghost is there to assist you",
                "friendly_ghost": 1
            },
            "image": pygame.transform.scale(game.image_loader.get_image("friend_ghost").subsurface(pygame.Rect(0, 0, game.settings.MOB_SIZE, game.settings.MOB_SIZE)), (game.settings.TILE_SIZE // 2, game.settings.TILE_SIZE // 2))
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
                "speed": 0.5
            },
            "image": pygame.transform.scale(game.image_loader.get_image("items").subsurface(pygame.Rect(33 * 32, 8 * 32, 32, 32)), (game.settings.TILE_SIZE, game.settings.TILE_SIZE))
        }



    def get_random_item(self, category):
        if DROP_LOOT_EVERYTIME: #FOR TESTING PURPOSES!
            if category == Categories.VERY_COMMON:
                return random.choice(list(self.very_commons.values()))
            return random.choice(list(self.legendaries.values()))
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