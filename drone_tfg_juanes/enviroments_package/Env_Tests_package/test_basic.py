from abc import ABC, abstractmethod


class TestStrategy(ABC):
    @abstractmethod
    def start_test(self, data: dict, time) -> None:
        pass

    @abstractmethod
    def get_reward(self, data: dict, time) -> (int, bool):
        """It returns the discrete reward and if it is terminated"""
        pass
