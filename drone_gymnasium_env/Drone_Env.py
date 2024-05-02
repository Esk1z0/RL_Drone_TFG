from gymnasium import Env
from gymnasium.spaces import Discrete, Box, Dict
import numpy as np
from drone_library.drone_simulation import Drone

class DroneCustomEnv(Env):
    metadata = {"render_modes": None, "render_fps": 0}

    def __init__(self):
        self.observation_space = Dict({
            "camera": Box(low=0, high=255, shape=(384000,)), #Image rgba of 400x240
            "IMU": Box(low=-1, high=1, shape=(4,)), #Quaternion
            "Sonar": Box(low=0, high=1) #distane from 0 to 1 with a range of 2 meters
        })
        self.action_space = Box(low=0, high=1, shape=(4,))
        self.render_mode = None
        self.drone = Drone()



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