import time

from robot_simulation import Bioloid
from .env_reward_package.reward_builder import RewardLoader
import numpy as np
from gymnasium import Env, spaces


class BioloidEnv(Env):
    """This class encapsulates the simulation_package to fit the gymnasium environment usage for training the agent"""
    def __init__(self, simulation_path, reward_json_path, options=None, no_render=True):
        """It builds the observation and action spaces, loads the reward function and launches the drone simulation

            Args:
                simulation_path (str): It tells where the webots simulation will be found
                reward_json_path (str): It tells where the reward function configuration is
        """

        self.observation_space = spaces.Dict({
            "back_left_1_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "back_left_2_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "back_left_3_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "back_right_1_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "back_right_2_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "back_right_3_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "front_left_1_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "front_left_2_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "front_left_3_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "front_right_1_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "front_right_2_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "front_right_3_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "head_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "neck_1_sensor": spaces.Box(low=-1.57, high=1.57, shape=(1,), dtype=np.float32),
            "neck_2_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "pelvis_sensor": spaces.Box(low=-3.14, high=3.14, shape=(1,), dtype=np.float32),
            "inertial unit": spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32),
            "gps": spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32),
            "compass": spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        })

        low = np.full((16,), -3.14, dtype=np.float32)
        high = np.full((16,), 3.14, dtype=np.float32)
        low[13] = -1.57
        high[13] = 1.57

        self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)

        self.bioloid = Bioloid(simulation_path, batch=True, realtime=True, stdout=True, stderr=True, no_rendering=no_render)

        self.reward_function_loader = RewardLoader(reward_json_path)
        self.reward_function_loader.load_packages()
        self.reward_function = None

        self.terminated = False

        self.first_reset = True
        self.closed = False

    def step(self, action) -> (dict, float, bool, bool, None):
        """Updates the environments with an action and returns the reward and observation asociated, also it returns if
        the environment is terminated or truncated.
        Args:
            action (np.array): It is the speed at which the motors will spin
        Returns:
            observation (dict): It is the environment observation
            reward (float): It is the environment reward associated with the action
            terminated (bool): Tells if the environment has terminated
            truncated (bool): Tells if the simulation crashed for some reason
            info (None): Not implemented
        """
        if self.closed or self.bioloid.is_sim_out():
            self.closed = False
            self.bioloid.start_simulation()

        reward, terminated, truncated = 0, False, False
        self.bioloid.send({"ACTION": "SET_ALL_MOTORS", "PARAMS": action})
        observation = self.bioloid.receive()

        truncated = self.is_truncated()
        if not truncated:
            reward, terminated = self._get_reward(observation)
        else:
            self.bioloid.end_simulation()

        return observation, reward, terminated, truncated, {}

    def reset(self, seed=None, options=None) -> (dict, None):
        """Tells the simulation to reset the drone physics and controller to restart the trainning
            Args:
                seed (int): It is useless with this environment, don't use it
                options (object): It is useless with this environment, don't use it
        """
        super().reset(seed=None)
        time.sleep(0.2)
        if self.first_reset or self.closed or self.bioloid.is_sim_out():
            self.closed = False
            self.first_reset = False
            self.bioloid.start_simulation()

        self.reward_function_loader.restart()
        self.reward_function = self.reward_function_loader.get_next_reward_function()

        self.bioloid.send({"ACTION": "RESET", "PARAMS": ""})

        obs = self.bioloid.receive()

        self.reward_function.start_reward(obs)

        return obs, {}

    def _get_reward(self, observation) -> (float, bool):
        """Returns the reward depending of the observation and the time from the internal tests and if the episode ended
            Args:
                observation (dict): The environment observation of the state
            Returns:
                reward (float): The reward given to the agent form its actions
                terminated (bool): The tests can terminate the episode if the drone fail the task
        """
        reward, terminated, change_reward_function = self.reward_function.get_reward(observation)
        if change_reward_function and not terminated:
            self.reward_function = self.reward_function_loader.get_next_reward_function()
            self.reward_function.start_reward(observation)
        return reward, terminated

    def is_truncated(self) -> bool:
        """Tells if the environment has crashed or closed for whatever reason"""
        return self.bioloid.is_sim_out()

    def close(self) -> None:
        """Close the simulation at the end of the training to make sure the environment doesn't stay opened"""
        if not self.bioloid.is_sim_out():
            self.bioloid.end_simulation()
        self.closed = True

    def int_to_binary_list(self, n, length=8):
        # Formatear el número a binario con longitud específica
        return [int(digit) for digit in f"{n:0{length}b}"]
