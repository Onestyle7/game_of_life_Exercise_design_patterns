import pygame
import numpy as np

class DrawManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.black = (0, 0, 0) 
        self.white = (255, 255, 255)  
        self.gray = (128, 128, 128)
        self.green = (0, 255, 0)

    def draw_button(self, x, y, width, height, text, color, text_color):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self, width, height, cell_width, cell_height, color):
        for y in range(0, height, cell_height):
            for x in range(0, width, cell_width):
                cell = pygame.Rect(x, y, cell_width, cell_height)
                pygame.draw.rect(self.screen, color, cell, 1)

    def draw_cells(self, game_state, cell_width, cell_height, n_cells_x, n_cells_y):
        for y in range(n_cells_y):
            for x in range(n_cells_x):
                cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                if game_state[x, y] == 1:
                    pygame.draw.rect(self.screen, self.black, cell)
