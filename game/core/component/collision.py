import pygame
from core.component.component import Component

class CollisionBox(Component):
    def attach(self, entity):
        self.entity = entity
        entity.collision_box = self

    @property
    def rect(self):
        return pygame.Rect(
            self.entity.position.x,
            self.entity.position.y,
            self.entity.sprite.width,
            self.entity.sprite.height
        )

    def place_meeting(self, x, y, cls, entities=None, ignore_self=True):
        """
        Check if the collision box of this entity collides with any entity of the specified class at the given position.
        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.
            cls (type): The class of the entities to check for collision.
            entities (list, optional): A list of entities to check against. If None, checks all entities of the class in the scene.
            ignore_self (bool): Whether to ignore the entity itself in the collision check.
        """
        if entities is None:
            entities = self.entity.scene.get_entities_by_class(cls)

        test_rect = pygame.Rect(x, y, self.rect.width, self.rect.height)
        for e in entities:
            if ignore_self and e is self.entity:
                continue
            if test_rect.colliderect(e.collision_box.rect):
                return True
        return False
