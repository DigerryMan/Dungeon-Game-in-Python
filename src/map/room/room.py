from items.lootable_item import LootableItem
from map.mob_spawner import MobSpawner
from map.room.room_drawer import RoomDrawer
from map.room.room_generator import RoomGenerator
from map.shop_stand import ShopStand
from map.trap_door import TrapDoor
from utils.directions import Directions

from ..block import Block
from ..chest import Chest
from .room_types import rooms, special_rooms


class Room:
    def __init__(self, room_type, game, doors_to_spawn: Directions, level):
        if room_type in special_rooms:
            self.layout = special_rooms[room_type]
        else:
            self.layout = rooms[room_type]

        self.game = game
        self.player = game.player
        self.level = level
        self.room_type = room_type
        self.is_cleared = False
        self.drawn_once = False
        self.doors_to_spawn = doors_to_spawn

        self.crucial_positions = []
        self.mob_spawner = MobSpawner(self, game)

        self.doors = []
        self.chest: Chest = None
        self.enemies = []
        self.blocks = []
        self.shop_stands = []
        self.walls = []
        self.items = []
        self.trap_door: TrapDoor = None

        self.room_generator = RoomGenerator(self)
        self.room_drawer = RoomDrawer(self)

    def get_objects(self):
        return {
            "doors": self.doors,
            "chest": self.chest,
            "enemies": self.enemies,
            "blocks": self.blocks,
            "shop_stands": self.shop_stands,
            "walls": self.walls,
            "items": self.items,
            "trap_door": self.trap_door,
        }

    def remove_item(self, item: LootableItem):
        self.items.remove(item)

    def remove_block(self, block: Block):
        self.blocks.remove(block)

    def remove_shop_stand(self, shop_stand: ShopStand):
        self.shop_stands.remove(shop_stand)

    def generate_room(self, entry_direction: Directions):
        if not self.drawn_once:
            self.room_generator.generate_room(entry_direction)

        self.spawn_player(entry_direction)
        self.player.spawn_pets()
        self.drawn_once = True

        if self.room_type == "boss" and not self.is_cleared:
            self.game.sound_manager.stop_with_fadeout("basementLoop", 1000)
            self.game.menu.display_boss_intro(self.enemies[0])
            self.game.sound_manager.play("bossEnter")
            self.game.sound_manager.play_with_fadein("bossFight", 1000, looped=True)

    def spawn_player(self, entry_direction):
        self.mob_spawner.spawn_player(entry_direction)

    def spawn_mob(self, mob_class, x, y, boss=None):
        self.mob_spawner.spawn_mob(mob_class, x, y, boss)

    def set_room_cleared(self):
        self.update_player_rooms_cleared()
        self.is_cleared = True
        self.enemies.clear()

        for door in self.doors:
            door.open()

        if self.chest and not self.chest.is_open:
            items_dropped = self.chest.open()
            for item in items_dropped:
                self.items.append(item)

        if self.trap_door:
            self.trap_door.open()

        if self.room_type == "boss":
            self.game.sound_manager.stop_with_fadeout("bossFight", 2000)
            self.game.sound_manager.play_with_fadein("basementLoop", 2000, looped=True)

    def update_player_rooms_cleared(self):
        if (
            not self.is_cleared
            and self.room_type != "start"
            and self.room_type != "shop"
        ):
            self.game.player.update_rooms_cleared()

    def get_block_layout(self):
        return self.layout

    def draw(self, screen):
        self.room_drawer.draw(screen)
