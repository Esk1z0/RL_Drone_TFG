from abc import ABC, abstractmethod


class FactoryModelInterface(ABC):
    @staticmethod
    @abstractmethod
    def class_name():
        """It returns the name used in the json config file for the reward function"""
        return "basic_factory_no_use_please"

    @abstractmethod
    def create_model(self):
        pass

    @abstractmethod
    def load_model(self):
        pass
