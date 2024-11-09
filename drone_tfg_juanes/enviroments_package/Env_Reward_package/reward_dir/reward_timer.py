from .reward_basic import RewardStrategyInterface
import numpy as np


class RewardTimer(RewardStrategyInterface):

    @staticmethod
    def class_name():
        return "timer"

    def __init__(self, max_time=1):
        self.max_time = max_time
        self.max_reward = 1
        self.start_time = 0

    def __str__(self):
        string = "name: Timer" \
                 "\ndescription: It sets the maximum time the drone can take to reach its goal"
        return string

    def start_test(self, obs: dict, motors:list, time) -> None:
        self.start_time = time

    def get_reward(self, obs: dict, motors:list, time) -> (int, bool, bool):
        reward, terminated, finish = self.max_reward, False, True
        if self._timeout(time):
            reward, terminated, finish = -1, True, False
        return reward, terminated, finish

    def teardown(self):
        pass

    def _timeout(self, time):
        return self.max_time < (time - self.start_time)