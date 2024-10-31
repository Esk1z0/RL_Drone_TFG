import gymnasium
from gymnasium import spaces
import numpy as np


class ScaleActionWrapper(gymnasium.ActionWrapper):
    def __init__(self, env, low=0, high=600):
        super().__init__(env)
        self.low = low
        self.high = high

        # Cambiar el espacio de acción para reflejar el rango de PPO
        self.action_space = spaces.Box(low=-1, high=1, shape=env.action_space.shape, dtype=np.float32)

    def action(self, action):
        # Reescalar de [-1, 1] al rango [low, high]
        scaled_action = self.low + (0.5 * (action + 1.0) * (self.high - self.low))
        return np.clip(scaled_action, self.low, self.high)  # Asegurar que esté en el rango

    def reverse_action(self, action):
        # Convertir de vuelta al rango [-1, 1] si es necesario
        return 2 * (action - self.low) / (self.high - self.low) - 1
