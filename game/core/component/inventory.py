from core.component.component import Component

class Inventory(Component):
    def __init__(self):
        super().__init__()
        self.items = {}

    def attach(self, entity):
        """
        Attach the component to an entity.

        Args:
            entity: The entity to attach the component to.
        """
        entity.inventory = self
        entity.components['inventory'] = self

    def add(self, item_name, qty=1):
        self.items[item_name] = self.items.get(item_name, 0) + qty

    def remove(self, item_name, qty=1):
        """
        Remove a specified quantity from inventory if possible
        Returns:
            bool: True if the item was successfully removed, False otherwise.
        """
        if self.items.get(item_name, 0) >= qty:
            self.items[item_name] -= qty
            if self.items[item_name] == 0:
                del self.items[item_name]
            return True
        return False

    def has(self, item_name):
        return self.items.get(item_name, 0) > 0
