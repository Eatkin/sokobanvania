from math import floor
from core.entity import Entity
from entities.pickup import PickUp
from entities.blocks import Solid, LockBlock
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

    def update(self):
        # Update input state
        self.input.update()

    def propose_move(self):
        dx = self.input.hinput
        dy = self.input.vinput
        if dx or dy:
            tx = self.position.x + dx * GRID_SIZE
            ty = self.position.y + dy * GRID_SIZE
            blocking_classes = self.collision_box.collides_with
            # Prioritise horizontal movement
            if abs(dx) > 0 and not self.scene.is_blocked(tx, self.position.y, blocking_classes):
                # Set our targets
                self.position.target = (tx, self.position.y)
                self.velocity.xspeed = dx * self.speed
            elif abs(dy) > 0 and not self.scene.is_blocked(self.position.x, ty, blocking_classes):
                # Set our targets
                self.position.target = (self.position.x, ty)
                self.velocity.yspeed = dy * self.speed

            if self.position.target:
                self.moving = True
                # Set occupancy
                self.scene.vacate(self.position.x, self.position.y, self)
                self.scene.occupy(self.position.target[0], self.position.target[1], self)

    def fixed_update(self):
        if not self.moving:
            self.propose_move()

        # Update previous position
        self.position.xprevious = self.position.x
        self.position.yprevious = self.position.y
        dt = PHYSICS_TICK_TIME

        if self.moving:
            self.update_sprite_direction()
            self.move_axis('x', dt)
            self.move_axis('y', dt)
            if self.check_target_reached():
                self.on_grid_snap()

        self.continuous_collision()

    def on_grid_snap(self):
        # Check for collision with pickups
        collisions = [PickUp, LockBlock]
        items = self.collision_box.instance_meeting_all(self.position.x, self.position.y, collisions)
        for item in items:
            if isinstance(item, PickUp):
                self.inventory.add(item.name)
                print(f"Picked up item: {item.name}")
                item.destroy()
            if isinstance(item, LockBlock):
                unlocks_with = item.item_required
                if self.inventory.has(unlocks_with):
                    self.inventory.remove(unlocks_with)
                    item.destroy()
                    print(f"Unlocked {item.__class__.__name__} with {unlocks_with}")

    def continuous_collision(self):
        # Handle any continuously required collision checks here e.g. monsters
        pass

    def on_inventory_change(self):
        """Update collision rules based on inventory changes."""
        self.collision_box.reset_collision_rules()
        to_remove = []
        for cls in self.collision_box.collides_with:
            if issubclass(cls, LockBlock) and self.inventory.has(cls.item_required):
                to_remove.append(cls)
                print(f"{cls.__name__} no longer solid thanks to {cls.item_required} in inventory")

        # Remove the items that are marked for removal
        while to_remove:
            self.collision_box.collides_with.remove(to_remove.pop())

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

    def update_sprite_direction(self):
        self.sprite.xflip = self.velocity.xspeed < 0

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
