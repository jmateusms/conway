# Rules
LOOP_WALLS = 0 # 1 = first and last rows/columns are neighbors, 0 = not neighbors
LOOP_PLAYER = 1 # 1 = player can move from one side to the other,
                # 0 = player can't move from one side to the other

# game dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 50

# colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# game settings
FPS = 60
DRAW_INTERVAL = 250 # in milliseconds
