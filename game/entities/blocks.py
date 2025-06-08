from core.entity import Entity
from entities.tiles import WaterTile, DirtTile
from core.component.position import Position
from core.component.movement import Movement
from core.component.sprite import Sprite
from core.component.collision import CollisionBox
from core.layer import LayerType
from common.sprites import SPRITES

class Solid(Entity):
    def __init__(self, x, y, sprite_info, components=None):
        super().__init__()
        self.add_component(Position(x, y))
        self.add_component(Sprite(sprite_info, components=components))

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

class RedLockBlock(LockBlock):
    item_required = 'red_key'
    def __init__(self, x, y):
        super().__init__(x, y, 'red_key')

class BlueLockBlock(LockBlock):
    item_required = 'blue_key'
    def __init__(self, x, y):
        super().__init__(x, y, 'blue_key')

class YellowLockBlock(LockBlock):
    item_required = 'yellow_key'
    def __init__(self, x, y):
        super().__init__(x, y, 'yellow_key')

# Pushable shit
class DirtBlock(Entity):
    def __init__(self, x, y):
        sprite_info = SPRITES['pushables']['dirt_block']
        super().__init__()
        self.add_component(Movement(x, y))
        self.add_component(Sprite(sprite_info))
        self.add_component(CollisionBox())

    def on_grid_snap(self):
        collisions = [WaterTile]
        collides_with = self.collision_box.instance_meeting_all(self.position.x, self.position.y, collisions)
        for c in collides_with:
            if isinstance(c, WaterTile):
                # Kill self, kill water and create a dirt tile in its place
                dirt = DirtTile(self.position.x, self.position.y)
                self.scene.add_entity_to_layer(dirt, LayerType.BACKGROUND)
                self.destroy()
                c.destroy()
                return
