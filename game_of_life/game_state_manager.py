import numpy as np
import pickle
import os

class GameStateManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameStateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.game_state = np.random.choice([0, 1], size=(40, 30), p=[0.6, 0.4])
        self.save_file_name = "savefile.pkl"

    def save_game_state(self):
        with open(self.save_file_name, 'wb') as file:
            pickle.dump(self.game_state, file)

    def load_game_state(self):
        if os.path.exists(self.save_file_name):
            with open(self.save_file_name, 'rb') as file:
                self.game_state = pickle.load(file)
        else:
            print(f"File {self.save_file_name} does not exist.")

    def toggle_cell_state(self, x, y):
        if 0 <= x < len(self.game_state) and 0 <= y < len(self.game_state[0]):
            self.game_state[x, y] = 1 - self.game_state[x, y]