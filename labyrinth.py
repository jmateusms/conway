import numpy as np
from settings import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, LOOP_WALLS

class Labyrinth:
    def __init__(self, width=SCREEN_WIDTH//CELL_SIZE, height=SCREEN_HEIGHT//CELL_SIZE, mode='labyrinth'):
        self.width = width
        self.height = height
        self.grid = np.zeros((self.height, self.width))
        self.start = None
        self.goal = None
        self.mode = mode # 'labyrinth' or 'conway'
        self.loop_walls = LOOP_WALLS

    def toggle_cell(self, x, y):
        self.grid[y][x] = 1 - self.grid[y][x]

    def set_start(self, x, y):
        self.start = (x, y)

    def set_goal(self, x, y):
        self.goal = (x, y)

    def get_neighbors(self, x, y):
        if self.loop_walls:
            neighbors = [
                ((x-1) % self.width, y),
                ((x+1) % self.width, y),
                (x, (y-1) % self.height),
                (x, (y+1) % self.height),
                ((x-1) % self.width, (y-1) % self.height),
                ((x+1) % self.width, (y+1) % self.height),
                ((x-1) % self.width, (y+1) % self.height),
                ((x+1) % self.width, (y-1) % self.height)
            ]
        else:
            neighbors = []
            if x > 0:
                neighbors.append((x-1, y))
            if x < self.width - 1:
                neighbors.append((x+1, y))
            if y > 0:
                neighbors.append((x, y-1))
            if y < self.height - 1:
                neighbors.append((x, y+1))
            if x > 0 and y > 0:
                neighbors.append((x-1, y-1))
            if x < self.width - 1 and y < self.height - 1:
                neighbors.append((x+1, y+1))
            if x > 0 and y < self.height - 1:
                neighbors.append((x-1, y+1))
            if x < self.width - 1 and y > 0:
                neighbors.append((x+1, y-1))
        return neighbors

    def conway_update(self):
        new_grid = self.grid.copy()
        for y in range(self.height):
            for x in range(self.width):
                total = sum([self.grid[ny][nx] for nx, ny in self.get_neighbors(x, y)])
                if self.grid[y][x] == 1:
                    if total < 2 or total > 3:
                        new_grid[y][x] = 0
                else:
                    if total == 3:
                        new_grid[y][x] = 1
        self.grid = new_grid

    def update(self, player_moved=False):
        if self.mode == 'labyrinth' and player_moved:
            self.conway_update()
        elif self.mode == 'conway':
            self.conway_update()
