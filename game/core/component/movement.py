from core.component.component import Component
from core.component.position import Position
from core.component.velocity import Velocity
from common.constants import GRID_SIZE, BASE_SPEED
from utils import sign

# Wrapper class for Position and Velocity components together
class Movement(Component):
    def __init__(self, x=0, y=0, xspeed=0, yspeed=0, movement_speed=BASE_SPEED):
        super().__init__()
        self.position = Position(x, y)
        self.velocity = Velocity(xspeed, yspeed, movement_speed)
        self.moving = False
        self.entity = None

    def attach(self, entity):
        self.position.attach(entity)
        self.velocity.attach(entity)
        entity.movement = self
        self.entity = entity

    # Utility functions
    def attempt_move(self, dx, dy, initiator):
        """
        Attempt to move the entity by dx, dy.
        If the movement is successful, it updates the position and velocity.
        If the movement is blocked, it does nothing.
        Args:
            dx (int): The change in x direction (in grid units).
            dy (int): The change in y direction (in grid units).
            initiator (Entity, optional): The entity that initiated the movement
        Returns:
            bool: True if the movement was successful, False otherwise.
        """
        if initiator.movement.moving:
            # If already moving, don't allow another move
            return False

        tx = initiator.position.x + dx * GRID_SIZE
        ty = initiator.position.y + dy * GRID_SIZE
        blocking_classes = initiator.collision_box.collides_with
        pushable_classes = initiator.collision_box.pushable_classes
        all_classes = blocking_classes + pushable_classes

        blockers = initiator.scene.is_blocked(tx, ty, blocking_classes=all_classes)
        # Check if there's any full blocking classes
        if any(isinstance(b, tuple(blocking_classes)) for b in blockers):
            return False

        # OPTIONAL: Set a entity.can_push method?
        # Check if there's any pushable classes using isinstance
        pushable = next((b for b in blockers if isinstance(b, tuple(pushable_classes))), None)

        if pushable is not None:
            if not pushable.movement.attempt_move(dx, dy, pushable):
                return False

        # If we reach here, move
        initiator.position.target = (tx, ty)
        initiator.velocity.xspeed = dx * initiator.velocity.speed
        initiator.velocity.yspeed = dy * initiator.velocity.speed
        initiator.movement.moving = True
        # Set occupancy
        initiator.scene.vacate(initiator.position.x, initiator.position.y, initiator)
        initiator.scene.occupy(initiator.position.target[0], initiator.position.target[1], initiator)
        return True


    def move_axis(self, axis: str, dt: float):
        speed = getattr(self.entity.velocity, f"{axis}speed")
        if speed == 0:
            return

        pos = getattr(self.entity.position, axis)
        next_pos = pos + speed * dt
        setattr(self.entity.position, axis, next_pos)

    def check_target_reached(self):
        if self._reached_target():
            self.entity.position.x, self.entity.position.y = self.entity.position.target
            self.entity.velocity.xspeed = 0
            self.entity.velocity.yspeed = 0
            self.entity.movement.moving = False
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
