from .reward_basic import RewardStrategyInterface
import numpy as np

class RewardPrintPosition(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "print_position_debug"

    def __init__(self):
        self.initial_position = None
        self.step_counter = 0

    def __str__(self):
        return (
            "name: Print GPS Position and Distance\n"
            "description: Imprime la posición actual, la distancia desde el inicio y el vector de dirección."
        )

    def start_test(self, obs: dict, time) -> None:
        self.initial_position = np.array(obs["gps"][:2])  # Guardamos X e Y del GPS
        self.step_counter = 0

    def get_reward(self, obs: dict, time) -> (float, bool, bool):
        self.step_counter += 1
        current_position = np.array(obs["gps"][:2])
        distance = np.linalg.norm(current_position - self.initial_position)
        direction_vector = current_position - self.initial_position

        print(f"\n--- STEP {self.step_counter} ---")
        print(f"Posición actual       : {current_position}")
        print(f"Distancia al inicio   : {distance:.4f}")
        print(f"Vector de dirección   : {direction_vector}")

        return 0.0, False, False  # Recompensa 0, sin terminar, sin cambiar estrategia

    def teardown(self):
        self.initial_position = None
        self.step_counter = 0
