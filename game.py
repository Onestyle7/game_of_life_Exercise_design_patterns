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

# Initialize Pygame
pygame.init()

tick_interval = 1000

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

def save_game_state(file_path, game_state):
    with open(file_path, 'wb') as file:
        pickle.dump(game_state, file)

def load_game_state(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)  

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
button_x, button_y = (width - button_width) // 2, height - button_height - 10

save_button_x, save_button_y = (width - button_width) // 2, button_y - 120
load_button_x, load_button_y = (width - button_width) // 2, button_y - 180

def draw_button():
    pygame.draw.rect(screen, green, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Next Generation", True, black)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

def draw_save_load_buttons():
    pygame.draw.rect(screen, green, (save_button_x, save_button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Save", True, black)
    screen.blit(text, (save_button_x + (button_width - text.get_width()) // 2, save_button_y + (button_height - text.get_height()) // 2))

    pygame.draw.rect(screen, green, (load_button_x, load_button_y, button_width, button_height))
    text = font.render("Load", True, black)
    screen.blit(text, (load_button_x + (button_width - text.get_width()) // 2, load_button_y + (button_height - text.get_height()) // 2))

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)

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

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)

running = True
#Track time since last update
last_update_time = 0
#initialization of the pause state
is_paused = False
pause_button_x, pause_button_y = (width - button_width) // 2, button_y - 60  # Adjust the position as needed

def draw_pause_button():
    text = "Pause" if not is_paused else "Resume"
    pygame.draw.rect(screen, green, ( pause_button_x, pause_button_y, button_width, button_height))
    font=pygame.font.Font(None, 36)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(pause_button_x + button_width // 2, pause_button_y + button_height // 2))
    screen.blit(text_surface, text_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the pause button is clicked
            if pause_button_x <= event.pos[0] <= pause_button_x + button_width and pause_button_y <= event.pos[1] <= pause_button_y + button_height:
                is_paused = not is_paused
            # Check if the next generation button is clicked
            elif button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                next_generation()
            # Check if the save button is clicked
            elif save_button_x <= event.pos[0] <= save_button_x + button_width and save_button_y <= event.pos[1] <= save_button_y + button_height:
                save_game_state("savefile.pkl", game_state)
            # Check if the load button is clicked
            elif load_button_x <= event.pos[0] <= load_button_x + button_width and load_button_y <= event.pos[1] <= load_button_y + button_height:
                game_state = load_game_state("savefile.pkl")
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]

    if not is_paused:
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > tick_interval:
            next_generation()
            last_update_time = current_time

    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button()
    draw_pause_button()
    draw_save_load_buttons()  # Draw save and load buttons

    pygame.display.flip()

pygame.quit()
