from test_no_roll import TestStrategy


class TestContext:
    def __init__(self, strategy: TestStrategy):
        self.strategy = strategy

    def run(self, data: dict) -> None:
        self.strategy.run_test(data)

    def get_results(self) -> dict:
        return self.strategy.get_results()
