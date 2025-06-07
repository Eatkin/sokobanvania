from core.component.component import Component
from core.component.position import Position
from core.component.velocity import Velocity
from common.constants import GRID_SIZE

# Wrapper class for Position and Velocity components together
class Movement(Component):
    def __init__(self, x=0, y=0, xspeed=0, yspeed=0):
        super().__init__()
        self.position = Position(x, y)
        self.velocity = Velocity(xspeed, yspeed)

    def attach(self, entity):
        self.position.attach(entity)
        self.velocity.attach(entity)
        entity.movement = self

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
        if initiator.moving:
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
        initiator.velocity.xspeed = dx * initiator.speed
        initiator.velocity.yspeed = dy * initiator.speed
        initiator.moving = True
        # Set occupancy
        initiator.scene.vacate(initiator.position.x, initiator.position.y, initiator)
        initiator.scene.occupy(initiator.position.target[0], initiator.position.target[1], initiator)
        return True
