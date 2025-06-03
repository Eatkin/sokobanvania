from entities.blocks import Solid, GreenLockBlock

LOCKBLOCKS = [GreenLockBlock]

DEFAULT_COLLISION_RULES = {
    "default": [Solid],
    "player": [Solid, *LOCKBLOCKS],
}
