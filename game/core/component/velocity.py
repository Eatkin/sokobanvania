from core.component.component import Component
from common.constants import BASE_SPEED

class Velocity(Component):
    def __init__(self, xspeed=0, yspeed=0, movement_speed=BASE_SPEED):
        super().__init__()
        self.xspeed = 0
        self.yspeed = 0
        self.speed = movement_speed

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.velocity = self
        entity.components['velocity'] = self
