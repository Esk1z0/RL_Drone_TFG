from .reward_basic import RewardStrategyInterface
import numpy as np


class RewardForwardDistance(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "forward_distance"

    def __init__(self, scale=1.0):
        self.initial_position = None
        self.last_distance = 0.0
        self.scale = scale  # Escalado de la recompensa para ajustarla si es necesario

    def __str__(self):
        return "name: Forward Distance\n" \
               "description: Recompensa basada en cuánto se aleja el robot de su posición inicial en el plano X-Y."

    def start_test(self, obs: dict, time) -> None:
        gps = obs["gps"]
        self.initial_position = np.array(gps[:2])  # Solo usamos X, Y
        self.last_distance = 0.0

    def get_reward(self, obs: dict, time) -> (float, bool, bool):
        current_position = np.array(obs["gps"][:2])  # Solo X, Y
        distance = np.linalg.norm(current_position - self.initial_position)

        # Recompensa incremental: diferencia de distancia desde la última llamada
        reward = (distance - self.last_distance) * self.scale
        self.last_distance = distance

        # No hay condiciones de terminación en esta recompensa
        terminated = False
        finish = False

        return reward, terminated, finish

    def teardown(self):
        self.initial_position = None
        self.last_distance = 0.0
