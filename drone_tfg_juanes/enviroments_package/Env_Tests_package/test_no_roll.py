from test_basic import TestStrategyBasic


class TestNoRoll(TestStrategyBasic):

    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        pass

    def teardown(self):
        pass
