from utils import sign
from core.entity import Entity
from core.input import get_input, KeyAction
from core.component.position import Position
from core.component.velocity import Velocity
from core.component.sprite import Sprite
from core import get_delta_time, GRID_SIZE
from common.sprites import SPRITES

class Player(Entity):
    def __init__(self, x, y):
        # Blue square
        super().__init__()
        self.add_component(Position(x, y))
        self.add_component(Velocity(0, 0))
        self.add_component(Sprite(SPRITES['player']['ball_dude']))
        self.speed = GRID_SIZE
        self.moving = False
        self.target_pos = (x, y)

    def update(self):
        dt = get_delta_time()
        input = get_input()

        if not self.moving:
            dx, dy = 0, 0
            dx = input['held'][KeyAction.KEY_RIGHT] - input['held'][KeyAction.KEY_LEFT]
            # Priority goes to horizontal movement
            if dx == 0:
                dy = input['held'][KeyAction.KEY_DOWN] - input['held'][KeyAction.KEY_UP]

            if dx or dy:
                self.velocity.xspeed = dx
                self.velocity.yspeed = dy
                self.target_pos = (
                    self.position.x + dx * GRID_SIZE,
                    self.position.y + dy * GRID_SIZE
                )
                self.moving = True

        if self.moving:
            vx = self.velocity.xspeed * self.speed * dt
            vy = self.velocity.yspeed * self.speed * dt
            self.position.x += vx
            self.position.y += vy

            # Check if we've reached or passed the target
            if self._reached_target():
                self.position.x, self.position.y = self.target_pos
                self.velocity.xspeed = 0
                self.velocity.yspeed = 0
                self.moving = False
                self.target_pos = None

    def _reached_target(self):
        if self.velocity.xspeed > 0 and self.position.x >= self.target_pos[0]:
            return True
        if self.velocity.xspeed < 0 and self.position.x <= self.target_pos[0]:
            return True
        if self.velocity.yspeed > 0 and self.position.y >= self.target_pos[1]:
            return True
        if self.velocity.yspeed < 0 and self.position.y <= self.target_pos[1]:
            return True
        return False
