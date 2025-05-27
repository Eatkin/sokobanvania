import time

_last_time = time.time()
DELTA_TIME = 0.0
GRID_SIZE = 32

def update_delta_time():
    global DELTA_TIME, _last_time
    current_time = time.time()
    DELTA_TIME = current_time - _last_time
    _last_time = current_time

def get_delta_time():
    return DELTA_TIME
