from core.entity import Entity
from entities.pickup import PickUp
from entities.blocks import LockBlock
from entities.tiles import DirtTile
from core.component.movement import Movement
from core.component.sprite import Sprite, Xflip
from core.component.input import InputParser
from core.component.collision import CollisionBox
from core.component.inventory import Inventory
from core.component.properties import Properties
from common.sprites import SPRITES

class Player(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.add_component(Movement(x, y))
        self.add_component(Sprite(SPRITES['player']['ball_dude'], components=[Xflip()]))
        self.add_component(InputParser())
        self.add_component(CollisionBox())
        self.add_component(Inventory())
        self.add_component(Properties())

    def staging_update(self):
        if self.movement.moving:
            return

        dx = self.input.hinput
        dy = self.input.vinput
        if dx:
            success = self.movement.attempt_move(dx, 0, self)
            if success:
                dy = 0
        if dy:
            success = self.movement.attempt_move(0, dy, self)

    def update(self):
        super().update()

    def fixed_update(self):
        super().fixed_update()
        self.continuous_collision()
        # More complex handling for sprites later
        self.update_sprite_direction()

    def on_grid_snap(self):
        # Check for collision with pickups etc
        collisions = [PickUp, LockBlock, DirtTile]
        items = self.collision_box.instance_meeting_all(self.position.x, self.position.y, collisions)
        for item in items:
            if isinstance(item, PickUp):
                self.inventory.add(item.name)
                print(f"Picked up item: {item.name}")
                item.destroy()
            elif isinstance(item, LockBlock):
                unlocks_with = item.item_required
                if self.inventory.has(unlocks_with):
                    self.inventory.remove(unlocks_with)
                    item.destroy()
                    print(f"Unlocked {item.__class__.__name__} with {unlocks_with}")
            elif isinstance(item, DirtTile):
                # Dirt tiles are converted to regular so just delete it
                item.destroy()

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

    def update_sprite_direction(self):
        if self.velocity.xspeed == 0:
            return
        self.sprite.xflip = self.velocity.xspeed < 0
