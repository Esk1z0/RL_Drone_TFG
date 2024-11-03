import gymnasium
from gymnasium import spaces
import numpy as np


class ScaleActionWrapper(gymnasium.ActionWrapper):
    def __init__(self, env, in_low=0, in_high=1, out_low=0, out_high=1):
        super().__init__(env)
        self.in_low = in_low
        self.in_high = in_high
        self.out_low = out_low
        self.out_high = out_high

        self.f1 = self.out_high - self.out_low
        self.f2 = self.in_high - self.in_low

        self.action_space = spaces.Box(low=in_low, high=in_high, shape=env.action_space.shape, dtype=np.float32)

    def action(self, action):

        action = np.clip(action, self.in_low, self.in_high)
        return self.out_low + self.f1 * (action - self.in_low) / self.f2

    def reverse_action(self, action):
        # Convertir de vuelta al rango [-1, 1] si es necesario
        return 2 * (action - self.low) / (self.high - self.low) - 1
