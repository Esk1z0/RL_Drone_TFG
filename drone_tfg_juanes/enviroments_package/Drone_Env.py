from drone_simulation import Drone
from .Env_Reward_package.reward_builder import RewardLoader
import numpy as np
from gymnasium import Env, spaces


class DroneEnv(Env):

    def __init__(self, simulation_path, reward_json_path):
        self.observation_space = spaces.Dict({
            "camera": spaces.Box(low=0, high=255, shape=(240, 400), dtype=np.uint8),
            "inertial unit": spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32),
            "left distance sensor": spaces.Box(low=0, high=1, dtype=np.float32),
            "right distance sensor": spaces.Box(low=0, high=1, dtype=np.float32),
            "altimeter": spaces.Box(low=0, high=np.inf, dtype=np.float32),
            "accelerometer": spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32),
            "gps": spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32),
            "command": spaces.MultiBinary(8)
        })
        self.action_space = spaces.Box(low=0, high=200, shape=(4,), dtype=np.float32)

        self.drone = Drone(simulation_path, batch=True, realtime=True, stdout=True, stderr=True)
        self.motors = [0, 0, 0, 0]
        self.drone.start_simulation()

        self.reward_function_loader = RewardLoader(reward_json_path)
        self.reward_function_loader.load_packages()
        self.reward_function = None

        self.terminated = False

    def step(self, action):
        #TODO comprobar si un pequenio delay ayuda al entrenamiento
        reward, terminated, truncated = 0, False, False

        self.drone.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": action})
        observation = self.get_obs()
        observation["command"] = self.reward_function.reward_command()

        truncated = self.is_truncated()
        if not truncated:
            reward, terminated = self.get_reward(observation)
        else:
            self.drone.end_simulation()

        return observation, reward, terminated, truncated, True

    def reset(self, seed=None, options=None):
        self.reward_function_loader.restart()
        self.reward_function = self.reward_function_loader.get_next_reward_function()

        self.drone.send({"ACTION": "RESET", "PARAMS": ""})
        self.motors = [0, 0, 0, 0]
        obs = self.get_obs()

        self.reward_function.start_reward(obs)
        return obs, None

    def get_reward(self, observation):
        reward, terminated, change_reward_function = self.reward_function.get_reward(observation)
        if change_reward_function and not terminated:
            self.reward_function = self.reward_function_loader.get_next_reward_function()
            self.reward_function.start_reward(observation)
        return reward, terminated

    def is_truncated(self):
        return self.drone.is_sim_out()

    def close(self):
        self.drone.end_simulation()

    def get_obs(self):
        return self.drone.receive()

