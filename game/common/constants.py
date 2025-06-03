from entities.blocks import Solid, GreenLockBlock, RedLockBlock, BlueLockBlock, YellowLockBlock

LOCKBLOCKS = [GreenLockBlock, RedLockBlock, BlueLockBlock, YellowLockBlock]

DEFAULT_COLLISION_RULES = {
    "default": [Solid],
    "player": [Solid, *LOCKBLOCKS],
}

GRID_SIZE = 32
