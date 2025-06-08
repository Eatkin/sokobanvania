from core import PHYSICS_TICK_TIME

class Entity:
    def __init__(self):
        self.components = {}
        self.layer = None
        self.scene = None

    def update(self):
        # General updates every frame
        pass

    def staging_update(self):
        # Prepare updates for the fixed update phase
        pass

    def fixed_update(self):
        # Fixed updates every physics tick (e.g., 60 FPS)
        # Movement handling
        if hasattr(self, 'movement'):
            self.position.xprevious = self.position.x
            self.position.yprevious = self.position.y

            if self.movement.moving:
                dt = PHYSICS_TICK_TIME
                self.movement.move_axis('x', dt)
                self.movement.move_axis('y', dt)
                if self.movement.check_target_reached():
                    self.on_grid_snap()

    def on_grid_snap(self):
        pass

    def draw(self, screen):
        if hasattr(self, 'sprite') and hasattr(self, 'position'):
            self.sprite.draw(screen, self.position)


    def add_component(self, component):
        """
        Add a component to the entity.

        Args:
            component: The component to add.
        """
        component.attach(self)

    def destroy(self):
        """
        Destroy the entity, removing it from the scene and cleaning up.
        """
        if self.scene:
            self.scene.remove_entity(self)

    def delete(self):
        """
        Destructor for behaviour on dereferencing the entity.
        """
        pass

    # Misc methods with no-op to prevent weird crashes
    def on_inventory_change(self):
        pass
