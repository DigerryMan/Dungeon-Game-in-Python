import pygame
from items.item_types import ItemType

class PlayerCollisionEngine():
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def correct_unvalid_move(self):
        self.player.rect.x += self.player.x_change
        self.collide_blocks('x')
        self.player.rect.y += self.player.y_change
        self.collide_blocks('y')
    
    def collide_blocks(self, direction_axis:str):
        rect_hits = pygame.sprite.spritecollide(self.player, self.game.collidables, False)
        if rect_hits:
            mask_hits = self.get_mask_colliding_sprite(rect_hits)
            if mask_hits: 
                if direction_axis == 'x':
                    self.player.rect.x -= self.player.x_change
                elif direction_axis == 'y':
                    self.player.rect.y -= self.player.y_change

    def get_mask_colliding_sprite(self, rect_hits):
        for sprite in rect_hits:
            if pygame.sprite.collide_mask(self.player, sprite):
                return sprite

    def check_items_pick_up(self):
        rect_hits = pygame.sprite.spritecollide(self.player, self.game.items, False)
        if rect_hits:
            items = [self.get_mask_colliding_sprite([rect_hit]) for rect_hit in rect_hits]
            for item in items:
                if item and not item.is_picked_up:
                    type, item_info = item.picked_up()
                    match type:
                        case ItemType.COIN:
                            self.player.coins += item_info
                        case ItemType.PICKUP_HEART:
                            self.player.heal(item_info)
                        case ItemType.ITEM:
                            self.player.eq.add_item(item_info)
                            item_image = pygame.transform.scale(item_info["image"], (self.game.settings.TILE_SIZE//1.3, self.game.settings.TILE_SIZE//1.3))
                            self.player.animation.prepare_item_pick_up_animation(item_image)
                        case ItemType.PILL:
                            self.player.eq.use_pill(item_info)
                        case ItemType.PICKUP_BOMB:
                            self.player.bombs += item_info