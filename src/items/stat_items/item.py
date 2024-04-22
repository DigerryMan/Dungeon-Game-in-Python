from items.lootable_item import LootableItem
from items.stat_items.items_list import ItemsList

class Item(LootableItem):
    def __init__(self, game, x, y, category):
        super().__init__(game, x, y)
        
        self.item = None

        self.roll_item(category)

        self.width = game.settings.TILE_SIZE
        self.height = game.settings.TILE_SIZE
        self.image = self.item["image"]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def roll_item(self, category):
        #self.item = self.game.items_list.get_random_item(category)
        self.item = self.game.items_list.epics["glass_cannon"]

    def picked_up(self):
        self.clean_up()
        return self.item