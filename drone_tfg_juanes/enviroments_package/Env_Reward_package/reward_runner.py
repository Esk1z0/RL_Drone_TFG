from reward_basic import RewardStrategyInterface


class TestContext:
    def __init__(self, strategy: RewardStrategyInterface):
        self.strategy = strategy

    def run(self, data: dict) -> None:
        self.strategy.run_test(data)

    def get_results(self) -> dict:
        return self.strategy.get_results()
