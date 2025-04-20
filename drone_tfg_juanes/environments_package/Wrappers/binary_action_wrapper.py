import gymnasium
import numpy as np
from gymnasium.spaces import Box


class BinaryActionWrapper(gymnasium.ActionWrapper):
    def __init__(self, env, power_level=288):
        """
        Convierte un espacio de acción continuo de [0, 576] en un espacio binario {0, 1}.
        Cuando se selecciona 1, el valor de potencia es power_level; cuando se selecciona 0, la potencia es 0.

        Args:
            env: Entorno de gymnasium.
            power_level: Valor que se asignará a los motores cuando la acción binaria sea 1.
        """
        super(BinaryActionWrapper, self).__init__(env)
        self.power_level = power_level
        # Cambiamos el espacio de acción a un espacio binario {0, 1} para cada motor
        self.action_space = Box(low=0, high=1, shape=(4,), dtype=np.int8)

    def action(self, action):
        """
        Convierte una acción binaria {0, 1} en un valor de potencia basado en power_level.

        Args:
            action: Acciones binarias {0, 1} para los 4 motores.

        Returns:
            Acción transformada donde 1 -> power_level y 0 -> 0.
        """
        # Convertimos la acción binaria a una acción de potencia
        converted_action = np.where(action == 1, self.power_level, 0)
        return converted_action
