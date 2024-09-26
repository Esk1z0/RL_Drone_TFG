from abc import ABC, abstractmethod


class RewardStrategyInterface(ABC):
    @abstractmethod
    def start_test(self, obs: dict, time) -> None:
        """It starts the test with the observations"""
        pass

    @abstractmethod
    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        """It returns the discrete reward, if the training failed (is terminated) and if it can finish"""
        pass

    @abstractmethod
    def teardown(self):
        """Clean everything on a reset or at the end of training"""
        pass
