from drone_tfg_juanes.simulation_package.controllers.xyz_controller.drone_library.drone_simulation import Drone

import numpy as np
from gymnasium import Env, spaces


class DroneEnv(Env):

    def __init__(self, simulation_dir):
        self.observation_space = spaces.Dict({
            "camera": spaces.Box(low=0, high=255, shape=(240, 400), dtype=np.uint8),
            "inertial unit": spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32),
            "left distance sensor": spaces.Box(low=0, high=1, dtype=np.float32),
            "right distance sensor": spaces.Box(low=0, high=1, dtype=np.float32),
            "altimeter": spaces.Box(low=0, high=np.inf, dtype=np.float32),
            "accelerometer": spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32),
            "command": spaces.MultiBinary(8)
        })

        self.action_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)

        self.drone = Drone(simulation_dir, batch=True, realtime=True)
        self.motors = [0, 0, 0, 0]
        self.drone.start_simulation()


    def step(self, action):
        reward, terminated = 0, True
        self.drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": action})
        observation = self.get_obs()
        observation["command"] = 00000000

        truncated = self.is_truncated()
        if not truncated:
            reward, terminated, command = self.get_reward(observation)
            observation["command"] = command

            if truncated:
                self.drone.end_simulation()
        return observation, reward, terminated, truncated, True

    def reset(self, seed=None, options=None):
        self.drone.send({"ACTION": "RESET", "PARAMS": ""})
        self.motors = [0, 0, 0, 0]
        return self.get_obs()

    def close(self):
        self.drone.end_simulation()

    def get_reward(self, observation):
        return 0, False, 00000000

    def is_truncated(self):
        return self.drone.is_sim_out()

    def get_obs(self):
        return self.drone.receive()


if __name__ == '__main__':
    lista = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    cadena = str(lista)
    print(cadena)
