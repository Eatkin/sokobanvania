import time

_last_time = time.time()
_accumulator = 0.0
DELTA_TIME = 0.0

FIXED_FPS = 60
PHYSICS_TICK_TIME = 1.0 / FIXED_FPS

def update_timing():
    global DELTA_TIME, _last_time, _accumulator

    now = time.time()
    frame_time = now - _last_time
    _last_time = now

    # Clamp to avoid spiral of death
    frame_time = min(frame_time, 0.25)

    DELTA_TIME = frame_time
    _accumulator += frame_time

def get_delta_time():
    return DELTA_TIME

def get_alpha():
    return _accumulator / PHYSICS_TICK_TIME

def is_physics_tick():
    global _accumulator
    if _accumulator >= PHYSICS_TICK_TIME:
        _accumulator -= PHYSICS_TICK_TIME
        return True
    return False
