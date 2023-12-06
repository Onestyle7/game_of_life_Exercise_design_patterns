# To create & start using python venv:
#       python -m venv venv
#       source venv/bin/activate

# Install specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic

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

# Deadline - 15th of December 2023
# Mail with: 
# 1. short screen recording demonstrating the new features
# 2. Linked code
# 3. Short description of the changes. Which design patterns you used and how you applied them. 

import pygame
import numpy as np
import pickle
from datetime import datetime
from draw import DrawManager
import os

# Initialize Pygame
pygame.init()

tick_interval = 1000
save_file_name = "savefile.pkl"

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
    
def save_game_state(game_state):
    with open(save_file_name, 'wb') as file:
        pickle.dump(game_state, file)

def load_game_state(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    else:
        print(f"File {file_path} does not exist.")
        return None

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.6, 0.4])

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
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

draw_manager = DrawManager(screen)

running = True
#Track time since last update
last_update_time = 0
#initialization of the pause state
is_paused = False
pause_button_x, pause_buttons_y = (width - button_width) // 2, buttons_y - 60



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if os.path.exists("savefile.pkl"):
                os.remove("savefile.pkl")
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the pause button is clicked
            if pause_button_x <= event.pos[0] <= pause_button_x + button_width and pause_buttons_y <= event.pos[1] <= pause_buttons_y + button_height:
                is_paused = not is_paused
            # Check if the next generation button is clicked
            elif button_x <= event.pos[0] <= button_x + button_width and buttons_y <= event.pos[1] <= buttons_y + button_height:
                next_generation()
            # Check if the save button is clicked
            elif save_button_x <= event.pos[0] <= save_button_x + button_width and save_buttons_y <= event.pos[1] <= save_buttons_y + button_height:
                save_game_state(game_state)
            # Check if the load button is clicked
            elif load_button_x <= event.pos[0] <= load_button_x + button_width and load_buttons_y <= event.pos[1] <= load_buttons_y + button_height:
                 loaded_state = load_game_state("savefile.pkl")
                 if loaded_state is not None:
                    game_state = loaded_state
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]

        if not is_paused:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > tick_interval:
                next_generation()
                last_update_time = current_time

    screen.fill(white)
    draw_manager.draw_grid(width, height, cell_width, cell_height, gray)
    draw_manager.draw_cells(game_state, cell_width, cell_height, n_cells_x, n_cells_y)
    draw_manager.draw_button(button_x, buttons_y, button_width, button_height, "Next Generation", green, black)
    draw_manager.draw_button(save_button_x, save_buttons_y, button_width, button_height, "Save", green, black)
    draw_manager.draw_button(load_button_x, load_buttons_y, button_width, button_height, "Load", green, black)
    draw_manager.draw_button(pause_button_x, pause_buttons_y, button_width, button_height, "Pause" if not is_paused else "Resume", green, black)

    pygame.display.flip()

pygame.quit()
