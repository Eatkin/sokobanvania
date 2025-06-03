import os
from entities.player import Player
from entities.pickup import PickUp
from entities.blocks import Block, GreenLockBlock, RedLockBlock, BlueLockBlock, YellowLockBlock
from common.constants import GRID_SIZE
from core.scene import BaseScene

legend = {
    'P': lambda x, y: Player(x * GRID_SIZE, y * GRID_SIZE),
    'C': lambda x, y: PickUp(x * GRID_SIZE, y * GRID_SIZE, 'chip'),
    # 'L': ChipSocket,
    # 'E': Exit,
    '#': lambda x, y: Block(x * GRID_SIZE, y * GRID_SIZE),
    '.': None,
    'y': lambda x, y: PickUp(x * GRID_SIZE, y * GRID_SIZE, 'yellow_key'),
    'g': lambda x, y: PickUp(x * GRID_SIZE, y * GRID_SIZE, 'green_key'),
    'r': lambda x, y: PickUp(x * GRID_SIZE, y * GRID_SIZE, 'red_key'),
    'b': lambda x, y: PickUp(x * GRID_SIZE, y * GRID_SIZE, 'blue_key'),
    'Y': lambda x, y: YellowLockBlock(x * GRID_SIZE, y * GRID_SIZE),
    'G': lambda x, y: GreenLockBlock(x * GRID_SIZE, y * GRID_SIZE),
    'R': lambda x, y: RedLockBlock(x * GRID_SIZE, y * GRID_SIZE),
    'B': lambda x, y: BlueLockBlock(x * GRID_SIZE, y * GRID_SIZE),
}

layers = {
    'P': 'player',
    'C': 'items',
    '#': 'game',
    '.': None,
    'y': 'items',
    'g': 'items',
    'r': 'items',
    'b': 'items',
    'Y': 'game',
    'G': 'game',
    'R': 'game',
    'B': 'game',
}

def get_level(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Level file '{path}' does not exist.")

    scene = BaseScene()

    y = 0
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            for x, char in enumerate(line):
                if char in legend:
                    entity = legend[char](x, y) if legend[char] else None
                    if entity:
                        l = layers.get(char)
                        if l:
                            scene.add_entity_to_layer(entity, l)

            y += 1

    return scene
