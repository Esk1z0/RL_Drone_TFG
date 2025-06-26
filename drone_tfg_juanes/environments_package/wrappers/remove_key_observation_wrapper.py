import gymnasium
from gymnasium import spaces


class RemoveKeyObservationWrapper(gymnasium.ObservationWrapper):
    """
        Elimina claves específicas del diccionario de observaciones del entorno.

        Args:
            env: Entorno de gymnasium que produce observaciones tipo dict.
            remove_keys: Lista de claves que se deben eliminar del diccionario de observaciones.
    """

    def __init__(self, env, remove_keys) -> None:
        super().__init__(env)
        self.remove_keys = remove_keys

        # Creamos un nuevo espacio de observación excluyendo las claves especificadas
        filtered_spaces = {
            key: space
            for key, space in self.observation_space.spaces.items()
            if key not in remove_keys
        }
        self.observation_space = spaces.Dict(filtered_spaces)

    def observation(self, observation) -> dict:
        """
        Elimina las claves indicadas del diccionario de observaciones.

        Args:
            observation: Diccionario de observación generado por el entorno base.

        Returns:
            Diccionario sin las claves especificadas en remove_keys.
        """
        return {
            key: value
            for key, value in observation.items()
            if key not in self.remove_keys
        }
