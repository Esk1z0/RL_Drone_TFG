from .reward_basic import RewardStrategyInterface


class RewardTimer(RewardStrategyInterface):

    @staticmethod
    def class_name():
        return "timer"

    def __init__(self, max_time=0):
        self.max_time = max_time

    def __str__(self):
        string = "name: Reward Timer" \
                 "\ndescription: It measures that the drone does not take too long to complete the task"
        return string


    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        pass

    def teardown(self):
        pass
