from reward_basic import RewardStrategyInterface


class RewardNoRoll(RewardStrategyInterface):

    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        pass

    def teardown(self):
        pass
