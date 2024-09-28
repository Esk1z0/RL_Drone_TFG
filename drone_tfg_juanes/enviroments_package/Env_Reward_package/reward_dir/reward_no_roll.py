from .reward_basic import RewardStrategyInterface


class RewardNoRoll(RewardStrategyInterface):

    @staticmethod
    def class_name():
        return "no_roll"

    def __init__(self, max_angle=0):
        self.max_angle = max_angle

    def __str__(self):
        string = "name: No Roll" \
                 "\ndescription: It measures that the drone does not tilt, or turn around, " \
                 "so it stays upwards"
        return string

    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        pass

    def teardown(self):
        pass
