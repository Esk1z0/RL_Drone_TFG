from abc import ABC, abstractmethod


class IProcess(ABC):

    @abstractmethod
    def process_data(self, data) -> dict:
        pass