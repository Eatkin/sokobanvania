from core.component.component import Component

class Velocity(Component):
    def __init__(self, xspeed=0, yspeed=0):
        super().__init__()
        self.xspeed = xspeed
        self.yspeed = yspeed

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.velocity = self
        entity.components['velocity'] = self
