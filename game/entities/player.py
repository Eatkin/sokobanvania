from math import floor
from core.entity import Entity, Solid
from entities.pickup import PickUp
from core.component.position import Position
from core.component.velocity import Velocity
from core.component.sprite import Sprite, Xflip
from core.component.input import InputParser
from core.component.collision import CollisionBox
from core.component.inventory import Inventory
from core import GRID_SIZE, PHYSICS_TICK_TIME
from common.sprites import SPRITES
from utils import sign

class Player(Entity):
    def __init__(self, x, y):
        # Blue square
        super().__init__()
        self.add_component(Position(x, y))
        self.add_component(Velocity(0, 0))
        self.add_component(Sprite(SPRITES['player']['ball_dude'], components=[Xflip()]))
        self.add_component(InputParser())
        self.add_component(CollisionBox())
        self.add_component(Inventory())
        self.speed = GRID_SIZE * 2
        self.moving = False
        self.target_pos = None

    def update(self):
        # Update input state
        self.input.update()

        if not self.moving:
            dx = self.input.hinput
            dy = self.input.vinput
            if dx or dy:
                self.velocity.xspeed = dx * self.speed
                self.velocity.yspeed = dy * self.speed
                self.target_pos = (
                    self.position.x + dx * GRID_SIZE,
                    self.position.y + dy * GRID_SIZE
                )
                self.moving = True

    def fixed_update(self):
        has_moved = self.position.x != self.position.xprevious or self.position.y != self.position.yprevious
        self.position.xprevious = self.position.x
        self.position.yprevious = self.position.y
        dt = PHYSICS_TICK_TIME

        if self.moving:
            self.update_sprite_direction()
            self.move_axis('x', dt)
            self.move_axis('y', dt)
            self.check_target_reached()
            if self.velocity.xspeed == 0 and self.velocity.yspeed == 0:
                self.moving = False
                self.target_pos = None
                # BUG IN THE MAKING: This doesn't actually check grid snap, it just checks the player has moved and then stopped
                # Realistically there shouldn't be any movement that doesn't snap to grid unless we die or something
                if has_moved:
                    self.on_grid_snap()

        else:
            self.target_pos = None
            self.moving = False

    def on_grid_snap(self):
        # Check for collision with pickups
        item = self.collision_box.instance_meeting(self.position.x, self.position.y, PickUp)
        if item is not None:
            self.inventory.add(item.name)
            print(f"Picked up item: {item.name}")
            item.destroy()

    def _reached_target(self):
        if self.velocity.xspeed > 0 and self.position.x >= self.target_pos[0]:
            return True
        if self.velocity.xspeed < 0 and self.position.x <= self.target_pos[0]:
            return True
        if self.velocity.yspeed > 0 and self.position.y >= self.target_pos[1]:
            return True
        if self.velocity.yspeed < 0 and self.position.y <= self.target_pos[1]:
            return True
        return False

    def update_sprite_direction(self):
        self.sprite.xflip = self.velocity.xspeed < 0

    def move_axis(self, axis: str, dt: float):
        speed = getattr(self.velocity, f"{axis}speed")
        if speed == 0:
            return

        pos = getattr(self.position, axis)
        next_pos = pos + speed * dt
        steps = floor(abs(next_pos - pos))
        residual = abs(next_pos - pos) - steps

        for i in range(1, steps+1):
            step = pos + sign(speed) * i
            if axis == 'x':
                blocked = self.collision_box.place_meeting(step, self.position.y, Solid)
            else:
                blocked = self.collision_box.place_meeting(self.position.x, step, Solid)

            if not blocked:
                setattr(self.position, axis, step)
            else:
                setattr(self.velocity, f"{axis}speed", 0)
                residual = 0
                break

        if residual > 0:
            step = getattr(self.position, axis) + sign(speed) * residual
            # We need to check min 1 pixel otherwise we get stuck
            check = getattr(self.position, axis) + sign(speed)
            if axis == 'x':
                blocked = self.collision_box.place_meeting(check, self.position.y, Solid)
            else:
                blocked = self.collision_box.place_meeting(self.position.x, check, Solid)

            if not blocked:
                setattr(self.position, axis, step)
            else:
                setattr(self.velocity, f"{axis}speed", 0)

    def check_target_reached(self):
        if self._reached_target():
            self.position.x, self.position.y = self.target_pos
            self.velocity.xspeed = 0
            self.velocity.yspeed = 0
            self.moving = False
            self.target_pos = None
