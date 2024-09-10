from abc import ABC, abstractmethod


class TestStrategy(ABC):
    @abstractmethod
    def run_test(self, data: dict) -> None:
        pass

    @abstractmethod
    def get_results(self) -> dict:
        pass

    def get_info(self) -> dict:
        pass
