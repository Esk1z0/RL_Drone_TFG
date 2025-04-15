import gymnasium
from gymnasium import spaces
import numpy as np


class ScaleActionWrapper(gymnasium.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)

        # Define el rango de entrada del agente (acción normalizada)
        self.in_low = np.full(env.action_space.shape, -1.0, dtype=np.float32)
        self.in_high = np.full(env.action_space.shape, 1.0, dtype=np.float32)

        # Define el rango real de cada motor
        self.out_low = np.full(env.action_space.shape, -3.14, dtype=np.float32)
        self.out_high = np.full(env.action_space.shape, 3.14, dtype=np.float32)
        self.out_low[13] = -1.57
        self.out_high[13] = 1.57

        # Precalcula los factores de escala para eficiencia
        self.f1 = self.out_high - self.out_low
        self.f2 = self.in_high - self.in_low

        # Cambia el action space del wrapper para que el agente trabaje en [-1, 1]
        self.action_space = spaces.Box(low=self.in_low, high=self.in_high, dtype=np.float32)

    def action(self, action):
        action = np.clip(action, self.in_low, self.in_high)
        return self.out_low + self.f1 * (action - self.in_low) / self.f2

    def reverse_action(self, action):
        return self.in_low + self.f2 * (action - self.out_low) / self.f1
