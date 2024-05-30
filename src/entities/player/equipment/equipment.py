import random
import json
import os
from entities.player.equipment.equipment_display import EquipmentDisplay

class Equipment():
    def __init__(self, player, game):
        self.import_stats_dicts()          
        self.player = player
        self.game = game
        
        #DISPLAY
        self.eq_display = EquipmentDisplay(self, game)

        #ITEMS
        self.items = []

    def import_stats_dicts(self):
        files_to_load = [
            "stats.json",
            "max_stats.json",
            "min_stats.json",
            "extra_stats.json",
            "extra_stats_max.json"
        ]
        for filename in files_to_load:
            path = os.path.join("entities", "player", "equipment", "eq_stats_dicts", filename)
            with open(path, 'r') as fp:
                setattr(self, filename.split('.')[0], json.load(fp))

    def draw(self, screen):
        self.eq_display.draw(screen)

    def user_eq_input(self, event_key):
        self.eq_display.change_highlighted_item(event_key)

    def add_item(self, item):
        try:
            index = self.items.index(item)
            self.items[index]["amount"] += 1
        except ValueError:
            item["amount"] = 1
            self.items.append(item)

        self.unpack_item(item)

    def use_pill(self, item):
        stats = item["stats"]
        for key, value in stats.items():
            if self.stats.get(key) is not None:
                val = random.choice(value)
                if self.extra_stats["PHD_obtained"]:
                    val = abs(val)

                self.stats[key] += val
                if self.stats[key] > self.max_stats[key]:
                    self.stats[key] = self.max_stats[key]
                if self.stats[key] < self.min_stats[key]:
                    self.stats[key] = self.min_stats[key]

        self.update_player_stats()

    def unpack_item(self, item):
        item_stats_dict = item["stats"]
        if item_stats_dict.get("description") is not None:
            self.unpack_item_with_description(item_stats_dict)
        else:
            self.unpack_item_with_stats(item_stats_dict)
            
    
    def unpack_item_with_description(self, item_stats_dict):
        for key, value in item_stats_dict.items():
            if key != "description" and self.extra_stats.get(key) is not None:
                if key.find("multiplier") != -1:
                    self.extra_stats[key] *= value
                else:
                    self.extra_stats[key] += value

                if self.extra_stats[key] > self.extra_stats_max[key]:
                    self.extra_stats[key] = self.extra_stats_max[key]
                elif key == "friendly_ghost":
                    self.player.spawn_pets(False)

    def unpack_item_with_stats(self, item_stats_dict):
        healValue = 0
        for key, value in item_stats_dict.items():
                if self.stats.get(key) is not None:
                    self.stats[key] += value
                    if self.stats[key] > self.max_stats[key]:
                        self.stats[key] = self.max_stats[key]
                    if self.stats[key] < self.min_stats[key]:
                        self.stats[key] = self.min_stats[key]    
                    if key == "health" and value > 0:
                        healValue = value
            
        self.update_player_stats()
        if healValue:
            self.player.heal(healValue)

    def update_player_stats(self):
        self.player.max_health = self.player.BASE_MAX_HEALTH + self.stats["health"] 
        if self.player.health > self.player.max_health:
            self.player.health = self.player.max_health
        self.player.speed = (self.player.BASE_SPEED + self.stats["speed"]) * self.game.settings.SCALE