from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np

class DroneCustomEnv(Env):
    metadata = {"render_modes": None, "render_fps": 0}

    def __init__(self):
        pass
    def step(self):
        pass
    def render(self):
        pass
    def reset(self):
        pass

    def close(self):
        pass
    def reward(self):
        pass


if __name__ == '__main__':
    lista = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    cadena = str(lista)
    print(cadena)