import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FPS, CELL_SIZE, \
    DRAW_INTERVAL, RED, GREEN, BLUE, LOOP_PLAYER, LOOP_WALLS
from labyrinth import Labyrinth
from player import Player
from buttons import Button

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Conway\'s Labyrinth')
clock = pygame.time.Clock()
last_draw_time = 0

def draw_labyrinth(labyrinth):
    """
    Render the labyrinth on the screen based on the labyrinth's grid.
    Cells with value 1 are drawn as black rectangles.
    """
    for y in range(labyrinth.height):
        for x in range(labyrinth.width):
            if labyrinth.grid[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(player):
    pygame.draw.circle(screen, RED, \
                       (player.x*CELL_SIZE + CELL_SIZE//2, \
                        player.y*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2 - 2)

def draw_goal(labyrinth):
    """
    Render the goal on the screen using a green color.
    """
    if labyrinth.goal:  # Check if the goal has been set
        x, y = labyrinth.goal
        pygame.draw.rect(screen, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def display_message(message, color=BLACK, size=30, y_offset=0):
    """
    Display a message on the screen.
    The message is centered both horizontally and vertically.
    """
    font = pygame.font.SysFont('arial', size)
    text = font.render(message, True, color)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, \
                       SCREEN_HEIGHT // 2 - text.get_height() // 2 + y_offset))

def main():
    global last_draw_time, CELL_SIZE, DRAW_INTERVAL, LOOP_PLAYER, LOOP_WALLS
    running = True
    mode = 'menu'
    auto_update_conway = False
    
    labyrinth = Labyrinth()
    labyrinth.set_goal(SCREEN_WIDTH // CELL_SIZE - 1, SCREEN_HEIGHT // CELL_SIZE - 1)
    player = Player()
    conway_button = Button(SCREEN_WIDTH // 2 - 70, \
                           SCREEN_HEIGHT // 2 - 100, 140, 40, 'Conway Simulation')
    increase_size_button = Button(SCREEN_WIDTH // 2 - 170, 
                                SCREEN_HEIGHT // 2 + 100, 140, 40, 'Increase Size')
    decrease_size_button = Button(SCREEN_WIDTH // 2 + 30, 
                                SCREEN_HEIGHT // 2 + 100, 140, 40, 'Decrease Size')
    instructions_button = Button(SCREEN_WIDTH // 2 - 70, 
                                SCREEN_HEIGHT // 2, 140, 40, 'Instructions')
    labyrinth_button = Button(SCREEN_WIDTH // 2 - 70, \
                                SCREEN_HEIGHT // 2 - 50, 140, 40, 'Labyrinth Game')
    toggle_player_loop_button = Button(SCREEN_WIDTH // 2 - 170, \
                                SCREEN_HEIGHT // 2 + 150, 140, 40, 'Toggle Player Loop')
    toggle_wall_loop_button = Button(SCREEN_WIDTH // 2 + 30, \
                                SCREEN_HEIGHT // 2 + 150, 140, 40, 'Toggle Wall Loop')
    setting_positions = 0 # 0: not setting, 1: setting player, 2: setting goal
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 'menu':
                    if conway_button.is_over(event.pos):
                        mode = 'conway'
                        labyrinth.mode = 'conway'
                    elif decrease_size_button.is_over(event.pos):
                        CELL_SIZE += 5
                        if CELL_SIZE > 100:
                            CELL_SIZE = 100
                        labyrinth = Labyrinth(width=SCREEN_WIDTH//CELL_SIZE, \
                                              height=SCREEN_HEIGHT//CELL_SIZE)
                        labyrinth.set_goal(SCREEN_WIDTH // CELL_SIZE - 1, \
                            SCREEN_HEIGHT // CELL_SIZE - 1)
                    elif increase_size_button.is_over(event.pos):
                        CELL_SIZE -= 5
                        if CELL_SIZE < 5:
                            CELL_SIZE = 5
                        labyrinth = Labyrinth(width=SCREEN_WIDTH//CELL_SIZE, \
                                              height=SCREEN_HEIGHT//CELL_SIZE)
                        labyrinth.set_goal(SCREEN_WIDTH // CELL_SIZE - 1, \
                            SCREEN_HEIGHT // CELL_SIZE - 1)
                    elif instructions_button.is_over(event.pos):
                        mode = 'instructions'
                    elif labyrinth_button.is_over(event.pos):
                            mode = 'labyrinth'
                            labyrinth.mode = 'labyrinth'
                    elif toggle_player_loop_button.is_over(event.pos):
                        LOOP_PLAYER = 1 - LOOP_PLAYER
                        player.loop_player = LOOP_PLAYER
                    elif toggle_wall_loop_button.is_over(event.pos):
                        LOOP_WALLS = 1 - LOOP_WALLS
                        labyrinth.loop_walls = LOOP_WALLS
                elif mode in ['labyrinth', 'conway']:
                    x, y = event.pos
                    if event.button == 1: # left click
                        labyrinth.toggle_cell(x // CELL_SIZE, y // CELL_SIZE)
                    elif event.button == 3: # right click
                        if mode == 'labyrinth':
                            if setting_positions == 0:
                                player.x, player.y = x // CELL_SIZE, y // CELL_SIZE
                                setting_positions = 1
                            elif setting_positions == 1:
                                labyrinth.set_goal(x // CELL_SIZE, y // CELL_SIZE)
                                setting_positions = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mode = 'menu'
                if mode == 'labyrinth':
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        dx, dy = {
                            pygame.K_LEFT: (-1, 0),
                            pygame.K_RIGHT: (1, 0),
                            pygame.K_UP: (0, -1),
                            pygame.K_DOWN: (0, 1)
                        }[event.key]
                        player.move(dx, dy, labyrinth)
                        labyrinth.update(True)
                        player.check_collision(labyrinth)
                    if event.key == pygame.K_r:
                        player = Player()
                        labyrinth = Labyrinth(width=SCREEN_WIDTH//CELL_SIZE, \
                                              height=SCREEN_HEIGHT//CELL_SIZE)
                        labyrinth.set_goal(\
                            SCREEN_WIDTH // CELL_SIZE - 1, SCREEN_HEIGHT // CELL_SIZE - 1)

                elif mode == 'conway':
                    if event.key == pygame.K_SPACE:
                        labyrinth.update()
                    elif event.key == pygame.K_e:
                        auto_update_conway = not auto_update_conway
                    elif event.key == pygame.K_r:
                        labyrinth = Labyrinth(width=SCREEN_WIDTH//CELL_SIZE, \
                                              height=SCREEN_HEIGHT//CELL_SIZE)
                        labyrinth.mode = 'conway'
                        auto_update_conway = False
                    elif event.key in [pygame.K_UP, pygame.K_RIGHT]:
                        DRAW_INTERVAL -= 50
                        if DRAW_INTERVAL < 50:
                            DRAW_INTERVAL = 50
                    elif event.key in [pygame.K_DOWN, pygame.K_LEFT]:
                        DRAW_INTERVAL += 50
                        if DRAW_INTERVAL > 1000:
                            DRAW_INTERVAL = 1000

        if mode == 'menu':
            conway_button.draw(screen)
            labyrinth_button.draw(screen)
            instructions_button.draw(screen)
            increase_size_button.draw(screen)
            decrease_size_button.draw(screen)
            toggle_player_loop_button.draw(screen)
            toggle_wall_loop_button.draw(screen)
            # Display current board size
            display_message(f"Board Size: {SCREEN_WIDTH//CELL_SIZE}x{SCREEN_HEIGHT//CELL_SIZE}", \
                            color=BLACK, size=25, y_offset=70)
            if LOOP_PLAYER:
                toggle_player_loop_button.text = 'Player Loop: ON'
            else:
                toggle_player_loop_button.text = 'Player Loop: OFF'
            if LOOP_WALLS:
                toggle_wall_loop_button.text = 'Wall Loop: ON'
            else:
                toggle_wall_loop_button.text = 'Wall Loop: OFF'

        elif mode == 'labyrinth':
            draw_labyrinth(labyrinth)
            draw_goal(labyrinth)
            draw_player(player)

            if player.state == 'dead':
                display_message("You died! Press 'R' to restart or 'M' for menu")
            elif player.state == 'win':
                display_message("You won! Press 'R' to restart or 'M' for menu")

        elif mode == 'instructions':
            display_message("Instructions:", color=BLACK, size=40, y_offset=-150)
            display_message("1. Use arrow keys to move.", color=BLACK, size=30, y_offset=-100)
            display_message("2. Avoid the walls.", color=BLACK, size=30, y_offset=-70)
            display_message("3. Reach the goal to win.", color=BLACK, size=30, y_offset=-40)
            display_message("Left click to place walls.", color=BLACK, size=30, y_offset=-10)
            display_message("[Labyrinth mode] Right click to place player and goal.", \
                            color=BLACK, size=30, y_offset=20)
            display_message("[Conway mode] Press 'Space' to update the board.", \
                            color=BLACK, size=30, y_offset=50)
            display_message("[Conway mode] Press 'E' to toggle automatic updates.", \
                            color=BLACK, size=30, y_offset=80)
            display_message("[Conway mode] Press UP/RIGHT to speed up updates.", \
                            color=BLACK, size=30, y_offset=110)
            display_message("[Conway mode] Press DOWN/LEFT to slow down updates.", \
                            color=BLACK, size=30, y_offset=140)
            display_message("Press 'R' to reset the board.", color=RED, size=30, y_offset=170)
            display_message("Press 'M' to return to the menu.", color=RED, size=30, y_offset=200)

        elif mode == 'conway':
            draw_labyrinth(labyrinth)
            if auto_update_conway:
                if pygame.time.get_ticks() - last_draw_time > DRAW_INTERVAL:
                    labyrinth.update()
                    last_draw_time = pygame.time.get_ticks()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
