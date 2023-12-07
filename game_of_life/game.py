# High-level logic
# 1. Create and init the simulation grid
# 2. Start the simulation with a tick interval of <n> seconds
# 3. At each tick:
#   3.1. Update the grid - loop over each element of the board
#   3.2. Render new generation

# General approach
# 1. Plan & write down the general workflow
#  1.1. Define Input&Output 
#  1.2. Consider adding validation
# 2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
# 3. Define communication between the objects
# 4. List the patterns you could apply
# 5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
#    and combine them into a complete application
# 6. Refine if needed

import pygame
import numpy as np
import os
from draw_factory import DrawFactory
from game_state_manager import GameStateManager

# Initialize Pygame
pygame.init()

tick_interval = 1000

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state manager
game_state_manager = GameStateManager()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

# Button dimensions
button_width, button_height = 200, 50
buttons_y = height - button_height - 10
button_x = (width - button_width) // 2
save_button_x = button_x - button_width - 10
load_button_x = button_x + button_width + 10
save_buttons_y = buttons_y
load_buttons_y = buttons_y

def next_generation():
    global game_state_manager
    new_state = np.copy(game_state_manager.game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state_manager.game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state_manager.game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state_manager.game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state_manager.game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state_manager.game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state_manager.game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state_manager.game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state_manager.game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state_manager.game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state_manager.game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state_manager.game_state = new_state


draw_factory = DrawFactory(screen)

running = True
# Track time since last update
last_update_time = 0
# Initialization of the pause state
is_paused = False
pause_button_x, pause_buttons_y = (width - button_width) // 2, buttons_y - 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button_x <= event.pos[0] <= pause_button_x + button_width and pause_buttons_y <= event.pos[1] <= pause_buttons_y + button_height:
                is_paused = not is_paused
            elif button_x <= event.pos[0] <= button_x + button_width and buttons_y <= event.pos[1] <= buttons_y + button_height:
                next_generation()
            elif save_button_x <= event.pos[0] <= save_button_x + button_width and save_buttons_y <= event.pos[1] <= save_buttons_y + button_height:
                game_state_manager.save_game_state()
            elif load_button_x <= event.pos[0] <= load_button_x + button_width and load_buttons_y <= event.pos[1] <= load_buttons_y + button_height:
                game_state_manager.load_game_state()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state_manager.toggle_cell_state(x, y)

        if not is_paused and pygame.time.get_ticks() - last_update_time > tick_interval:
            next_generation()
            last_update_time = pygame.time.get_ticks()

    screen.fill(white)
    draw_factory.draw_grid(width, height, cell_width, cell_height, gray)
    draw_factory.draw_cells(game_state_manager.game_state, cell_width, cell_height, n_cells_x, n_cells_y)
    draw_factory.draw_button(button_x, buttons_y, button_width, button_height, "Next Generation", green, black)
    draw_factory.draw_button(save_button_x, save_buttons_y, button_width, button_height, "Save", green, black)
    draw_factory.draw_button(load_button_x, load_buttons_y, button_width, button_height, "Load", green, black)
    draw_factory.draw_button(pause_button_x, pause_buttons_y, button_width, button_height, "Pause" if not is_paused else "Resume", green, black)

    pygame.display.flip()

pygame.quit()
