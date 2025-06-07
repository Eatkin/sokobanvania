from core import PHYSICS_TICK_TIME
from core.entity import Entity
from core.component.position import Position
from core.component.movement import Movement
from core.component.sprite import Sprite
from core.component.collision import CollisionBox
from common.sprites import SPRITES
from common.constants import BASE_SPEED
from utils import sign

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
        self.moving = False
        self.speed = BASE_SPEED

    # DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF DON'T REPEAT YOURSELF
    def fixed_update(self):
        self.position.xprevious = self.position.x
        self.position.yprevious = self.position.y
        dt = PHYSICS_TICK_TIME

        if self.moving:
            self.move_axis('x', dt)
            self.move_axis('y', dt)
            self.check_target_reached()


    def move_axis(self, axis: str, dt: float):
        speed = getattr(self.velocity, f"{axis}speed")
        if speed == 0:
            return

        pos = getattr(self.position, axis)
        next_pos = pos + speed * dt
        setattr(self.position, axis, next_pos)

    def check_target_reached(self):
        if self._reached_target():
            self.position.x, self.position.y = self.position.target
            self.velocity.xspeed = 0
            self.velocity.yspeed = 0
            self.moving = False
            self.position.target = None
            return True
        return False

    def _reached_target(self):
        if sign(self.velocity.xspeed) == 1 and self.position.x >= self.position.target[0]:
            return True
        if sign(self.velocity.xspeed) == -1 and self.position.x <= self.position.target[0]:
            return True
        if sign(self.velocity.yspeed) == 1 and self.position.y >= self.position.target[1]:
            return True
        if sign(self.velocity.yspeed) == -1 and self.position.y <= self.position.target[1]:
            return True
        return False
