from .reward_basic import RewardStrategyInterface
import numpy as np

class RewardForwardDistanceDelta(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "forward_distance_delta"

    def __init__(self, scale=1.0, penalty=-0.1, max_idle_steps=20, min_movement=0.001):
        self.initial_position = None
        self.last_position = None
        self.scale = scale
        self.penalty = penalty
        self.max_idle_steps = max_idle_steps
        self.min_movement = min_movement
        self.idle_counter = 0
        self.target_direction = np.array([1.0, 1.0]) / np.sqrt(2)  # Vector (1,1) normalizado

    def __str__(self):
        return (
            "name: Forward Distance with Inactivity Termination\n"
            "description: Recompensa avance en la dirección (1,1). Termina el episodio si no se detecta movimiento."
        )

    def start_test(self, obs: dict, time) -> None:
        pos = np.array(obs["gps"][:2])  # Solo X-Y
        self.initial_position = pos
        self.last_position = pos
        self.idle_counter = 0

    def get_reward(self, obs: dict, time) -> (float, bool, bool):
        current_position = np.array(obs["gps"][:2])
        delta = current_position - self.last_position
        projection = np.dot(delta, self.target_direction)

        if projection > self.min_movement:
            reward = projection * self.scale
            self.idle_counter = 0
        else:
            reward = self.penalty
            self.idle_counter += 1

        terminated = False
        if self.idle_counter >= self.max_idle_steps:
            reward += self.penalty
            terminated = True
            self.idle_counter = 0  # opcional: reinicio si reinicias el entorno manualmente

        self.last_position = current_position
        finish = False
        return reward, terminated, finish

    def teardown(self):
        self.initial_position = None
        self.last_position = None
        self.idle_counter = 0
