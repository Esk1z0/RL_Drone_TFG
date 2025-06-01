from .reward_basic import RewardStrategyInterface
import numpy as np


class RewardForwardDistanceDelta(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "forward_distance_delta"

    def __init__(self, scale=1.0, penalty=-0.1, max_idle_steps=20, min_movement=0.001):
        """
        Args:
            scale (float): Escala de la recompensa por moverse hacia adelante.
            penalty (float): Penalización cuando no se detecta movimiento.
            max_idle_steps (int): Número máximo de pasos sin movimiento antes de penalizar.
            min_movement (float): Movimiento mínimo que se considera como avance.
        """
        self.initial_position = None
        self.last_position = None
        self.scale = scale
        self.penalty = penalty
        self.max_idle_steps = max_idle_steps
        self.min_movement = min_movement
        self.idle_counter = 0

    def __str__(self):
        return (
            "name: Forward Distance with Inactivity Penalty\n"
            "description: Recompensa el avance en el plano X-Y. Penaliza si no se ha movido durante varios pasos."
        )

    def start_test(self, obs: dict, time) -> None:
        pos = np.array(obs["gps"][:2])  # Solo X-Y
        self.initial_position = pos
        self.last_position = pos
        self.idle_counter = 0

    def get_reward(self, obs: dict, time) -> (float, bool, bool):
        current_position = np.array(obs["gps"][:2])
        displacement = np.linalg.norm(current_position - self.last_position)

        if displacement > self.min_movement:
            reward = displacement * self.scale
            self.idle_counter = 0
        else:
            self.idle_counter += 1
            reward = 0.0

        if self.idle_counter >= self.max_idle_steps:
            reward += self.penalty
            self.idle_counter = 0  # Reiniciamos para no penalizar en cada paso siguiente

        self.last_position = current_position

        terminated = False
        finish = False
        return reward, terminated, finish

    def teardown(self):
        self.initial_position = None
        self.last_position = None
        self.idle_counter = 0
