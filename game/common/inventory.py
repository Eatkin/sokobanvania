from dataclasses import dataclass
from enum import Enum

class InventoryType(Enum):
    NONE = 0
    INVENTORY = 1
    EQUIPMENT = 2

# Class to encapsulate things that can be in the inventory
@dataclass(frozen=True)
class InventoryItem:
    name: str
    description: str
    item_type: InventoryType
    sprite: str = None  # Placeholder will use SpriteInfo later

INVENTORY_ITEMS = {
    "green_key": InventoryItem(
        name="Green Key",
        description="A key that opens green doors.",
        item_type=InventoryType.INVENTORY
    ),
    "red_key": InventoryItem(
        name="Red Key",
        description="A key that opens red doors.",
        item_type=InventoryType.INVENTORY
    ),
    "blue_key": InventoryItem(
        name="Blue Key",
        description="A key that opens blue doors.",
        item_type=InventoryType.INVENTORY
    ),
    "yellow_key": InventoryItem(
        name="Yellow Key",
        description="A key that opens yellow doors.",
        item_type=InventoryType.INVENTORY
    ),
}
