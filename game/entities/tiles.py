from core.entity import Entity
from core.component.position import Position
from core.component.sprite import Sprite
from core.component.collision import CollisionBox
from common.sprites import SPRITES

class Tile(Entity):
    def __init__(self, x, y, sprite_info, components=None):
        super().__init__()
        self.add_component(Position(x, y))
        self.add_component(Sprite(sprite_info, components=components))
        self.add_component(CollisionBox())

        # Add components
        if components:
            for component in components:
                self.add_component(component)

class DirtTile(Tile):
    def __init__(self, x, y):
        sprite = SPRITES['tiles']['dirt_tile']
        super().__init__(x, y, sprite_info=sprite)

class WaterTile(Tile):
    def __init__(self, x, y):
        sprite = SPRITES['tiles']['water_tile']
        super().__init__(x, y, sprite_info=sprite)
