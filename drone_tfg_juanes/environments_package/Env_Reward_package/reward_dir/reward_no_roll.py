from .reward_basic import RewardStrategyInterface
import numpy as np


class RewardNoRoll(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "no_roll"

    def __init__(self, max_angle=0, max_reward=1):
        self.max_angle = max_angle
        self.max_reward = max_reward
        self.vertical_q = np.array([0, 0, 0, 1])

    def __str__(self):
        string = "name: No Roll" \
                 "\ndescription: It measures that the drone does not tilt, or turn around, " \
                 "so it stays upwards"
        return string

    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        reward, terminated, finish = 0, False, True
        q2 = obs["inertial unit"]
        angle = self._quaternion_shortest_angle(self.vertical_q, q2)
        reward = self._calculate_angle_reward(angle)
        if reward < 0:
            terminated, finish = True, False
        return reward, terminated, finish

    def teardown(self):
        pass

    def _quaternion_shortest_angle(self, q1, q2):
        """
        Calcula el ángulo más corto en grados entre dos cuaterniones.
        """
        # Convertir a arrays de NumPy y normalizar los cuaterniones
        q1 = np.array(q1, dtype=np.float64)
        q2 = np.array(q2, dtype=np.float64)
        q1 /= np.linalg.norm(q1)
        q2 /= np.linalg.norm(q2)

        # Calcular el producto punto absoluto
        dot_product = abs(np.dot(q1, q2))
        # Asegurar que el valor esté en el rango válido [-1, 1] para arccos
        dot_product = np.clip(dot_product, -1.0, 1.0)

        # Calcular el ángulo
        angle_rad = 2 * np.arccos(dot_product)
        angle_deg = np.degrees(angle_rad)

        # Asegurar que el ángulo esté en el rango [0, 180]
        if angle_deg > 180:
            angle_deg = 360 - angle_deg

        return angle_deg

    def _calculate_angle_reward(self, angle_deg):
        if angle_deg <= self.max_angle / 2:
            # De 0° a mitad del ángulo máximo, la recompensa disminuye de max_reward a 0
            reward = self.max_reward * (1 - (2 * angle_deg / self.max_angle))
        elif angle_deg <= self.max_angle:
            # De mitad a ángulo máximo, la recompensa disminuye de 0 a -max_reward
            reward = -self.max_reward * ((2 * angle_deg / self.max_angle) - 1)
        else:
            # Si el ángulo excede el máximo permitido, asigna la recompensa negativa máxima
            reward = -self.max_reward
        return reward
