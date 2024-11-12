from .reward_basic import RewardStrategyInterface


class RewardHeight(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "height"

    def __init__(self, ideal_height=1, max_reward=1, tolerance_range=0.5, penalty_scale=0.1):
        self.ideal_height = ideal_height
        self.max_reward = max_reward
        self.tolerance_range = tolerance_range
        self.penalty_scale = penalty_scale

    def __str__(self):
        string = "name: Height" \
                 "\ndescription: It gives more reward the higher it gets, until it surpasses the ideal height and then " \
                 "it starts penalizing"
        return string

    def start_test(self, obs: dict, motors:list, time) -> None:
        pass

    def get_reward(self, obs: dict, motors:list, time) -> (int, bool, bool):
        altitude = obs["altimeter"][0]
        height_diff = abs(self.ideal_height-altitude)

        if height_diff <= self.tolerance_range:
            reward = self.max_reward * (1 - (height_diff / self.tolerance_range))
        else:
            reward = -self.penalty_scale * (height_diff - self.tolerance_range)

        return reward, False, False

    def teardown(self):
        pass
