from .reward_basic import RewardStrategyInterface


class RewardTimer(RewardStrategyInterface):

    @staticmethod
    def class_name():
        return "timer"

    def __init__(self, max_time=0):
        self.max_time = max_time
        self.start_time = 0

    def __str__(self):
        string = "name: Reward Timer" \
                 "\ndescription: It measures that the drone does not take too long to complete the task"
        return string

    def start_test(self, obs: dict, time) -> None:
        self.start_time = time

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        reward, terminated, finish = 1, False, True
        if self.max_time <= (time - self.start_time):
            reward, terminated, finish = -1, True, True
        return reward, terminated, finish

    def teardown(self):
        pass
