from test_basic import TestStrategy


class TestNoRoll(TestStrategy):


    def start_test(self, data: dict, time) -> None:
        pass

    def get_reward(self, data: dict, time) -> (int, bool):
        pass