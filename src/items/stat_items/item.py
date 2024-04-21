from items.lootable_item import LootableItem
from items.stat_items.items_list import ItemsList

class Item(LootableItem):
    def __init__(self, game, x, y, category):
        super().__init__(game, x, y)

        self.item = None

        self.roll_item(category)

        self.image = self.item["image"]


    def roll_item(self, category):
        self.item = self.game.items_list.commons[0]

    def picked_up(self):
        self.clean_up()
        return self.item