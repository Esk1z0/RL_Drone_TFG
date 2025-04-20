from .reward_basic import RewardStrategyInterface
import numpy as np

class RewardMotorInactivityPenalty(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "motor_inactivity_penalty"

    def __init__(self, motor_names=None, threshold_total=0.1, penalty=-0.02, max_inactive_steps=30):
        """
        Penaliza si el movimiento combinado de los motores es demasiado bajo.

        Args:
            motor_names (list): Lista de nombres de motores a observar.
            threshold_total (float): Mínimo movimiento total requerido para evitar penalización.
            penalty (float): Penalización cuando el movimiento total es bajo.
            max_inactive_steps (int): Número máximo de pasos con inactividad antes de terminar el episodio.
        """
        self.motor_names = motor_names or []
        self.threshold_total = threshold_total
        self.penalty = penalty
        self.max_inactive_steps = max_inactive_steps
        self.inactive_steps = 0
        self.last_positions = {}

    def __str__(self):
        return (
            "name: Motor Inactivity Penalty\n"
            "description: Penaliza cuando el movimiento combinado de todos los motores es insuficiente durante varios pasos consecutivos."
        )

    def start_test(self, obs: dict, time) -> None:
        self.last_positions = {
            name: np.array(obs[name]) for name in self.motor_names
        }
        self.inactive_steps = 0

    def get_reward(self, obs: dict, time) -> (float, bool, bool):
        total_delta = 0.0

        for name in self.motor_names:
            current = np.array(obs[name])
            last = self.last_positions[name]
            delta = np.linalg.norm(current - last)
            total_delta += delta
            self.last_positions[name] = current

        if total_delta < self.threshold_total:
            self.inactive_steps += 1
            reward = self.penalty
        else:
            self.inactive_steps = 0
            reward = 0.0

        terminated = self.inactive_steps >= self.max_inactive_steps

        return reward, terminated, False

    def teardown(self):
        self.last_positions = {}
        self.inactive_steps = 0
