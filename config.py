# WAREHOUSE SIZE

WIDTH = 800
HEIGHT = 600

GRID_SIZE = 20

ROWS = HEIGHT // GRID_SIZE
COLS = WIDTH // GRID_SIZE


# DEFAULT PARAMETERS

MAX_SPEED = 60
SAFE_DISTANCE = 40
TIME_STEP = 1


# WAREHOUSE SHELVES / OBSTACLES

OBSTACLES = [

    # x, y, width, height

    (200, 100, 80, 250),

    (400, 50, 80, 300),

    (600, 200, 80, 250),

    (100, 400, 200, 80),

    (450, 450, 200, 80)
]
# MOVING OBSTACLES

MOVING_OBSTACLES = [

    {
        "x": 150,
        "y": 150,
        "dx": 2,
        "dy": 0,
        "size": 25
    },

    {
        "x": 500,
        "y": 300,
        "dx": 0,
        "dy": 2,
        "size": 25
    }
]