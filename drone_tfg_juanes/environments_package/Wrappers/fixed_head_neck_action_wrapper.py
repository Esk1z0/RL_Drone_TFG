import gymnasium as gym
import numpy as np

class FixHeadNeckActionWrapper(gym.ActionWrapper):
    """
    Fija valores específicos para los motores de cabeza y cuello,
    ignorando los valores que proponga el agente para esos índices.
    """
    def __init__(self, env, fixed_values=None):
        super().__init__(env)
        # Índices según el orden de tu action_space (16 valores)
        self.head_index = 12
        self.neck_1_index = 13
        self.neck_2_index = 14

        # Valores fijos por defecto (puedes ajustarlos)
        self.fixed_values = fixed_values or {
            self.head_index: 0.0,
            self.neck_1_index: 0.0,
            self.neck_2_index: 0.0
        }

    def action(self, action):
        # Sobrescribe los valores fijos en la acción
        modified_action = np.array(action, dtype=np.float32)
        for idx, val in self.fixed_values.items():
            modified_action[idx] = val
        return modified_action
