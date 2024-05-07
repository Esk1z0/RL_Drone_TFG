from gymnasium import Env
from gymnasium.spaces import Discrete, Box, Dict
import numpy as np
from drone_library.drone_simulation import Drone


class DroneBaseEnv(Env):
    metadata = {"render_modes": None, "render_fps": 0}

    def __init__(self):
        self.observation_space = Dict({
            "camera": Box(low=0, high=255, shape=(384000,)),  # Image rgba of 400x240
            "IMU": Box(low=-1, high=1, shape=(4,)),  # Quaternion
            "Sonar": Box(low=0, high=1)  # distane from 0 to 1 with a range of 2 meters
        })
        self.action_space = Box(low=0, high=1, shape=(4,))
        self.render_mode = None
        self.drone = Drone()
        self.motors = [0, 0, 0, 0]

    def step(self, action):
        truncated = self.drone.send_receive({"ACTION": "SET_ALL_MOTORS", "PARAMS": action})
        observation = self._get_obs()
        reward, terminated = self.reward()
        return observation, reward, terminated, truncated, self.drone.get_actions()

    def render(self):
        pass

    def reset(self, seed=None, options=None):
        self.motors = [0, 0, 0, 0]
        self.drone.send_receive({"ACTION": "RESET", "PARAMS": ""})
        observation = self._get_obs()
        return observation

    def close(self):
        self.drone.end_simulation()

    def reward(self):
        pass

    def _get_obs(self):
        return self.drone.send_receive({"ACTION": "GET_DATA", "PARAMS": ""})


if __name__ == '__main__':
    lista = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    cadena = str(lista)
    print(cadena)
