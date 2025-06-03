from core.component.component import Component

class Velocity(Component):
    def __init__(self, xspeed, yspeed):
        super().__init__()
        self.xspeed = 0
        self.yspeed = 0

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.velocity = self
        entity.components['velocity'] = self
