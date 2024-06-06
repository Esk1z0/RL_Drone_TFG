from gymnasium import Env
from gymnasium.spaces import Box, Dict
from drone_simulation import Drone


class DroneBaseEnv(Env):
    metadata = {"render_modes": None, "render_fps": 0}

    def __init__(self, maxtime, command):
        self.observation_space = Dict({
            "camera": Box(low=0, high=255, shape=(384000,)),  # Image rgba of 400x240
            "IMU": Box(low=-1, high=1, shape=(4,)),  # Quaternion
            "Sonar": Box(low=0, high=1)  # distane from 0 to 1 with a range of 2 meters
        })
        self.action_space = Box(low=0, high=1, shape=(4,))
        self.render_mode = None
        self.drone = Drone()
        self.motors = [0, 0, 0, 0]

        self.maxtime = maxtime
        self.command = command

        self.drone.start_simulation()

    def step(self, action):
        reward, terminated = 0, True
        self.drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": action})
        observation = self.get_obs()
        observation["command"] = self.command
        truncated = self.is_truncated()
        if not truncated:
            reward, terminated = self.reward(observation)
        return observation, reward, terminated, truncated, self.drone.get_actions()

    def render(self):
        pass

    def reset(self, seed=None, options=None):
        self.motors = [0, 0, 0, 0]
        self.drone.send({"ACTION": "RESET", "PARAMS": ""})
        observation = self.get_obs()
        return observation

    def close(self):
        self.drone.end_simulation()

    def reward(self, observation):
        pass

    def is_truncated(self):
        return self.drone.is_sim_out()

    def get_obs(self):
        return self.drone.send({"ACTION": "GET_DATA", "PARAMS": ""})


if __name__ == '__main__':
    lista = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
    cadena = str(lista)
    print(cadena)
