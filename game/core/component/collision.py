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

    def _collision_at(self, x, y, cls, entities=None, ignore_self=True):
        if entities is None:
            entities = self.entity.scene.get_entities_by_class(cls)

        test_rect = pygame.Rect(x, y, self.rect.width, self.rect.height)
        for e in entities:
            if ignore_self and e is self.entity:
                continue
            if test_rect.colliderect(e.collision_box.rect):
                yield e

    def place_meeting(self, x, y, cls, entities=None, ignore_self=True):
        return any(self._collision_at(x, y, cls, entities, ignore_self))

    def instance_meeting(self, x, y, cls, entities=None, ignore_self=True):
        return next(self._collision_at(x, y, cls, entities, ignore_self), None)
