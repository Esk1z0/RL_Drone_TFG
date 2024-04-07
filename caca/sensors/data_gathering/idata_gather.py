from abc import ABC, abstractmethod


class IDataGather(ABC):

    @abstractmethod
    def __init__(self, device):
        pass

    @abstractmethod
    def get_data(self) -> dict:
        pass
