from .reward_basic import RewardStrategyInterface
import numpy as np


class RewardForwardWithPenalty(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "forward_with_penalty"

    def __init__(self, scale=1.0, inactivity_penalty=-0.01, min_movement=0.001, max_idle_steps=20):
        self.scale = scale
        self.inactivity_penalty = inactivity_penalty
        self.min_movement = min_movement
        self.max_idle_steps = max_idle_steps
        self.idle_counter = 0
        self.last_position = None

    def __str__(self):
        return (
            "name: Forward Movement + Inactivity Penalty\n"
            "description: Recompensa el avance en el plano X-Y y penaliza de forma acumulativa la inactividad."
        )

    def start_test(self, obs: dict, time) -> None:
        pos = np.array(obs["gps"][:2])
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
            reward = self.inactivity_penalty * self.idle_counter  # penalización acumulativa

        self.last_position = current_position
        return reward, False, False

    def teardown(self):
        self.last_position = None
        self.idle_counter = 0
