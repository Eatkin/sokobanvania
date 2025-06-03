from core.entity import Entity
from common.sprites import SPRITES
from core.component.position import Position
from core.component.sprite import Sprite
from core.component.collision import CollisionBox

class PickUp(Entity):
    def __init__(self, x, y, name):
        super().__init__()
        if name not in SPRITES['items']:
            raise ValueError(f"Item '{name}' does not exist in SPRITES['items']")
        self.name = name
        sprite_info = SPRITES['items'][name]
        self.add_component(Position(x, y))
        self.add_component(Sprite(sprite_info))
        self.add_component(CollisionBox())
