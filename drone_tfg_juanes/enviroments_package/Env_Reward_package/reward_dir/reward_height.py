from .reward_basic import RewardStrategyInterface


class RewardHeight(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "height"

    def __init__(self, ideal_height=0, max_reward=1):
        self.ideal_height = ideal_height
        self.max_reward = max_reward

    def __str__(self):
        string = "name: Height" \
                 "\ndescription: It gives more reward the higher it gets, until it surpasses the ideal height and then " \
                 "it starts penalizing"
        return string

    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        altitude = obs["altimeter"][0]
        reward = 0
        terminated = False
        if altitude > self.ideal_height:
            reward = -self.ideal_height
            terminated = True
        else:
            reward = (altitude / self.ideal_height) * self.max_reward
        print(reward)
        return reward, terminated, False

    def teardown(self):
        pass
