from .factory_model_base import FactoryModelInterface


class FactoryModelSAC(FactoryModelInterface):
    @staticmethod
    def class_name():
        return "SAC"

    def create_model(self):
        pass

    def load_model(self):
        pass
