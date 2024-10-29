import gymnasium
from gymnasium import ObservationWrapper
from gymnasium import spaces
import numpy as np


class RemoveKeyObservationWrapper(ObservationWrapper):
    def __init__(self, env, remove_key):
        super().__init__(env)
        # Guardar la clave a eliminar
        self.remove_key = remove_key

        # Crear un nuevo Dict sin la clave que deseas eliminar
        filtered_spaces = {key: space for key, space in self.observation_space.spaces.items() if key != remove_key}
        self.observation_space = spaces.Dict(filtered_spaces)

    def observation(self, observation):
        # Eliminar la clave del diccionario de observación
        return {key: value for key, value in observation.items() if key != self.remove_key}


