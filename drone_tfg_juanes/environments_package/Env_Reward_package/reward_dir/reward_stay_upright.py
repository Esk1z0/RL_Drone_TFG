from .reward_basic import RewardStrategyInterface
import numpy as np


class RewardStayUpright(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "stay_upright"

    def __init__(self, max_angle=45, survival_bonus=0.005, fall_penalty=-1.0):
        self.max_angle = max_angle
        self.survival_bonus = survival_bonus
        self.fall_penalty = fall_penalty
        self.vertical_q = np.array([0, 0, 0, 1])

    def __str__(self):
        return (
            "name: Stay Upright\n"
            "description: Recompensa ligeramente si el agente no se vuelca y termina el episodio si el ángulo supera un umbral."
        )

    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (float, bool, bool):
        q2 = np.array(obs["inertial unit"])
        angle = self._quaternion_shortest_angle(self.vertical_q, q2)

        if angle > self.max_angle:
            return self.fall_penalty, True, False
        return self.survival_bonus, False, False

    def teardown(self):
        pass

    def _quaternion_shortest_angle(self, q1, q2):
        q1 = np.array(q1, dtype=np.float64)
        q2 = np.array(q2, dtype=np.float64)
        q1 /= np.linalg.norm(q1)
        q2 /= np.linalg.norm(q2)
        dot_product = abs(np.dot(q1, q2))
        dot_product = np.clip(dot_product, -1.0, 1.0)
        angle_rad = 2 * np.arccos(dot_product)
        angle_deg = np.degrees(angle_rad)
        return min(angle_deg, 360 - angle_deg)
