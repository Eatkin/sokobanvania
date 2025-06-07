from entities.blocks import (
    Solid,
    LockBlock,
    GreenLockBlock,
    RedLockBlock,
    BlueLockBlock,
    YellowLockBlock,
    DirtBlock
)

LOCKBLOCKS = [GreenLockBlock, RedLockBlock, BlueLockBlock, YellowLockBlock]

DEFAULT_COLLISION_RULES = {
    "default": [Solid, DirtBlock, LockBlock],
    "player": [Solid, *LOCKBLOCKS],
}

DEFAULT_PUSH_RULES = {
    "default": [],
    "player": [DirtBlock]
}
