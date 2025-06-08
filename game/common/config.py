from entities.blocks import (
    Solid,
    LockBlock,
    GreenLockBlock,
    RedLockBlock,
    BlueLockBlock,
    YellowLockBlock,
    DirtBlock
)
from entities.tiles import (
    DirtTile,
    WaterTile
)

LOCKBLOCKS = [GreenLockBlock, RedLockBlock, BlueLockBlock, YellowLockBlock]

COLLISION_DEFAULT = [Solid, DirtBlock, LockBlock]
DEFAULT_COLLISION_RULES = {
    "default": COLLISION_DEFAULT,
    "player": [Solid, *LOCKBLOCKS],
    "dirtblock": [Solid, DirtBlock, DirtTile],
}

PUSH_DEFAULT = []
DEFAULT_PUSH_RULES = {
    "default": PUSH_DEFAULT,
    "player": [DirtBlock]
}
