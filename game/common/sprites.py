from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class SpriteInfo:
    path: str                           # Path to the image
    alpha_channel: bool = True          # Whether we need transparency
    offset: Tuple[int, int] = (0, 0)    # Optional offset for positioning
    is_animation: bool = False          # Flag to check if this is an animation
    frame_count: int = 1                # Number of frames in the animation
    frame_width: int = 0                # Width of each frame in the strip
    frame_height: int = 0               # Height of each frame in the strip
    frame_speed: float = 0.1            # Time between frames in seconds (for animation)

SPRITES = {
    "player": {
        "ball_dude": SpriteInfo(
            path="assets/sprites/player/ball_dude.png",
        ),
    },
    "tiles": {
        "floor_tile": SpriteInfo(
            path="assets/tiles/floor_tile.png",
            alpha_channel=False
        ),
        "wall_tile": SpriteInfo(
            path="assets/tiles/wall.png",
            alpha_channel=False
        )
    },
    "items": {
        "green_key": SpriteInfo(
            path="assets/sprites/items/green_key.png",
        )
    },
    "lock_blocks": {
        # These reference the item required to unlock them
        "green_key": SpriteInfo(
            path="assets/tiles/green_lock_block.png",
            alpha_channel=False
        ),
    }
}
