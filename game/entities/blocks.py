from core.entity import Entity
from core.component.position import Position
from core.component.sprite import Sprite
from core.component.collision import CollisionBox
from common.sprites import SPRITES

class Solid(Entity):
    def __init__(self, x, y, sprite_info, components=None):
        super().__init__()
        self.add_component(Position(x, y))
        self.add_component(Sprite(sprite_info, components=components))
        self.add_component(CollisionBox())

        # Add components
        if components:
            for component in components:
                self.add_component(component)

class Block(Solid):
    def __init__(self, x, y):
        sprite = SPRITES['tiles']['wall_tile']
        super().__init__(x, y, sprite_info=sprite)


class LockBlock(Entity):
    def __init__(self, x, y, item_required):
        super().__init__()
        if item_required not in SPRITES['lock_blocks']:
            raise ValueError(f"Item '{item_required}' does not exist in SPRITES['lock_blocks']")
        self.item_required = item_required
        sprite_info = SPRITES['lock_blocks'][item_required]
        self.add_component(Position(x, y))
        self.add_component(Sprite(sprite_info))
        self.add_component(CollisionBox())

# Dummy classes for collision rules
class GreenLockBlock(LockBlock):
    item_required = 'green_key'
    def __init__(self, x, y):
        super().__init__(x, y, 'green_key')
