from .reward_basic import RewardStrategyInterface
import numpy as np

class RewardMotorInactivityPenalty(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "motor_inactivity_penalty"

    def __init__(self, motor_names=None, threshold=0.01, penalty=-0.02):
        self.motor_names = motor_names or []
        self.last_positions = {}
        self.threshold = threshold  # Cambios menores a esto se consideran "sin movimiento"
        self.penalty = penalty

    def __str__(self):
        return (
            "name: Motor Inactivity Penalty\n"
            "description: Penaliza cuando los motores no se mueven lo suficiente entre pasos."
        )

    def start_test(self, obs: dict, time) -> None:
        self.last_positions = {
            name: np.array(obs[name]) for name in self.motor_names
        }

    def get_reward(self, obs: dict, time) -> (float, bool, bool):
        inactive_count = 0

        for name in self.motor_names:
            current = np.array(obs[name])
            last = self.last_positions[name]
            delta = np.linalg.norm(current - last)
            if delta < self.threshold:
                inactive_count += 1
            self.last_positions[name] = current

        # Penaliza proporcionalmente al número de motores inactivos
        reward = self.penalty * inactive_count

        return reward, False, False

    def teardown(self):
        self.last_positions = {}