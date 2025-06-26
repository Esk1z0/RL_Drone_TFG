import gymnasium
from gymnasium import spaces
import numpy as np


class ScaleActionWrapper(gymnasium.ActionWrapper):
    """
    Escala las acciones del agente desde el rango normalizado [-1, 1] al rango real
    que espera el entorno, definido para cada motor.

    Este wrapper permite que el agente trabaje con acciones más estandarizadas (por ejemplo, [-1, 1])
    mientras el entorno recibe valores físicos realistas como ángulos en radianes.

    Args:
        env: Entorno de Gymnasium con espacio de acción tipo Box.
    """

    def __init__(self, env) -> None:
        super().__init__(env)

        # Define el rango de entrada esperado por el agente: acciones normalizadas [-1, 1]
        self.in_low = np.full(env.action_space.shape, -1.0, dtype=np.float32)
        self.in_high = np.full(env.action_space.shape, 1.0, dtype=np.float32)

        # Define el rango real de cada motor (ángulos en radianes)
        self.out_low = np.full(env.action_space.shape, -3.14, dtype=np.float32)
        self.out_high = np.full(env.action_space.shape, 3.14, dtype=np.float32)
        self.out_low[13] = -1.57  # Cuello eje 1
        self.out_high[13] = 1.57

        # Precalcula los factores de escala para eficiencia
        self.f1 = self.out_high - self.out_low
        self.f2 = self.in_high - self.in_low

        # Redefine el espacio de acción para que el agente trabaje en el rango [-1, 1]
        self.action_space = spaces.Box(low=self.in_low, high=self.in_high, dtype=np.float32)

    def action(self, action) -> np.ndarray:
        """
        Escala la acción del agente del rango [-1, 1] al rango físico esperado por el entorno.

        Args:
            action (np.ndarray): Acción normalizada del agente.

        Returns:
            np.ndarray: Acción transformada al rango físico del entorno.
        """
        action = np.clip(action, self.in_low, self.in_high)
        return self.out_low + self.f1 * (action - self.in_low) / self.f2

    def reverse_action(self, action) -> np.ndarray:
        """
        Convierte una acción del entorno de vuelta al rango normalizado [-1, 1].

        Útil para análisis o interpretaciones externas de la política del agente.

        Args:
            action (np.ndarray): Acción en el rango físico del entorno.

        Returns:
            np.ndarray: Acción escalada al rango [-1, 1].
        """
        return self.in_low + self.f2 * (action - self.out_low) / self.f1
