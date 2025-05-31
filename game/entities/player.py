from core.entity import Entity, Solid
from core.component.position import Position
from core.component.velocity import Velocity
from core.component.sprite import Sprite, Xflip
from core.component.input import InputParser
from core.component.collision import CollisionBox
from core import GRID_SIZE, PHYSICS_TICK_TIME
from common.sprites import SPRITES
from utils import sign

class Player(Entity):
    def __init__(self, x, y):
        # Blue square
        super().__init__()
        self.add_component(Position(x, y))
        self.add_component(Velocity(0, 0))
        self.add_component(Sprite(SPRITES['player']['ball_dude'], components=[Xflip()]))
        self.add_component(InputParser())
        self.add_component(CollisionBox())
        self.speed = GRID_SIZE
        self.moving = False
        self.target_pos = (x, y)

    def update(self):
        # Update input state
        self.input.update()

        if not self.moving:
            dx = self.input.hinput
            dy = self.input.vinput
            if dx or dy:
                self.velocity.xspeed = dx * self.speed
                self.velocity.yspeed = dy * self.speed
                self.target_pos = (
                    self.position.x + dx * GRID_SIZE,
                    self.position.y + dy * GRID_SIZE
                )
                self.moving = True

    def fixed_update(self):
        # ALWAYS set previous position before moving
        self.position.xprevious = self.position.x
        self.position.yprevious = self.position.y

        dt = PHYSICS_TICK_TIME
        if self.moving:
            # Flip sprite if moving left
            if self.velocity.xspeed < 0:
                self.sprite.xflip = True
            else:
                self.sprite.xflip = False

            # Collision checking
            # TODO: For loop to move upto 1px at a time for precise movement
            next_x = self.position.x + sign(self.velocity.xspeed)
            next_y = self.position.y + sign(self.velocity.yspeed)
            if self.velocity.xspeed != 0 and not self.collision_box.place_meeting(next_x, self.position.y, Solid):
                self.position.x = next_x
                self.velocity.yspeed = 0  # cancel vertical speed if horizontal move successful
            else:
                self.velocity.xspeed = 0

            if not self.collision_box.place_meeting(self.position.x, next_y, Solid):
                self.position.y = next_y
            else:
                self.velocity.yspeed = 0

            if self.velocity.xspeed != 0 or self.velocity.yspeed != 0:
                vx = self.velocity.xspeed * dt
                vy = self.velocity.yspeed * dt
                self.position.x += vx
                self.position.y += vy

                # Check if we've reached or passed the target
                if self._reached_target():
                    self.position.x, self.position.y = self.target_pos
                    self.velocity.xspeed = 0
                    self.velocity.yspeed = 0
                    self.moving = False
                    self.target_pos = None
            else:
                # If not moving, reset target position
                self.target_pos = (self.position.x, self.position.y)
                self.moving = False

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
