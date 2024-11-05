from .reward_basic import RewardStrategyInterface
import numpy as np


class RewardZone(RewardStrategyInterface):

    @staticmethod
    def class_name():
        return "zone"

    def __init__(self, max_distance=1, max_reward=1):
        self.max_distance = max_distance
        self.max_reward = max_reward
        self.origin = np.array([0, 0])

    def __str__(self):
        string = "name: Zone" \
                 "\ndescription: It measures that the drone does not escape from a certain area respect" \
                 "its original coordinates. It only measures the horizontal area, not the height"
        return string

    def start_test(self, obs: dict, time) -> None:
        self.origin = np.array(obs["gps"][:-1])

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        reward, terminated, finish = 0, False, True

        distance = np.linalg.norm(np.array(obs["gps"][:-1]) - self.origin)
        if distance > self.max_distance:
            reward, terminated, finish = -1, True, False
        else:
            reward = self.max_reward * (1 - distance/self.max_distance)

        return reward, terminated, finish

    def teardown(self):
        pass
