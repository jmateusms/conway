from settings import LOOP_PLAYER

class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.state = 'alive'
        self.loop_player = LOOP_PLAYER

    def move(self, dx, dy, labyrinth):
        if self.loop_player:
            new_x = self.x + dx
            new_y = self.y + dy
            if new_x < 0:
                new_x = labyrinth.width - 1
            elif new_x >= labyrinth.width:
                new_x = 0
            if new_y < 0:
                new_y = labyrinth.height - 1
            elif new_y >= labyrinth.height:
                new_y = 0
        else:
            if 0 <= self.x + dx < labyrinth.width:
                new_x = self.x + dx
            if 0 <= self.y + dy < labyrinth.height:
                new_y = self.y + dy
        
        self.x = new_x
        self.y = new_y

    def check_collision(self, labyrinth):
        if labyrinth.grid[self.y][self.x] == 1:
            self.state = 'dead'
        elif (self.x, self.y) == labyrinth.goal:
            self.state = 'win'
