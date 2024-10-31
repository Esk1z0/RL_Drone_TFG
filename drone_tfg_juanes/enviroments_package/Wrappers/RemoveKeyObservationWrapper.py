import gymnasium
from gymnasium import spaces
import numpy as np


class RemoveKeyObservationWrapper(gymnasium.ObservationWrapper):
    def __init__(self, env, remove_keys):
        super().__init__(env)
        # Guardar la clave a eliminar
        self.remove_keys = remove_keys

        # Crear un nuevo Dict sin la clave que deseas eliminar
        filtered_spaces = {key: space for key, space in self.observation_space.spaces.items() if key not in remove_keys}
        self.observation_space = spaces.Dict(filtered_spaces)

    def observation(self, observation):
        # Eliminar la clave del diccionario de observación
        return {key: value for key, value in observation.items() if key not in self.remove_keys}


