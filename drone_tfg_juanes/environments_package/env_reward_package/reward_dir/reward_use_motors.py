from .reward_basic import RewardStrategyInterface


class RewardUseMotors(RewardStrategyInterface):
    @staticmethod
    def class_name():
        return "use_motors"

    def __init__(self, max_reward=1, penalty_factor=0.5):
        self.max_reward = max_reward
        self.prev_motors = [0,0,0,0]
        self.penalty_factor = penalty_factor

    def __str__(self):
        string = "name: Use Motors" \
                 "\ndescription: It gives more reward the more you use the motors, the higher the value, and the higher " \
                 "the more motors are being used"
        return string

    def start_test(self, obs: dict, motors:list, time) -> None:
        self.prev_motors = motors

    def get_reward(self, obs: dict, motors: list, time) -> (float, bool, bool):
        motor_usage = sum(motors) / len(motors)
        # Penaliza la variación en el uso de motores
        motor_variation = sum(abs(m - prev_m) for m, prev_m in zip(motors, self.prev_motors)) / len(motors)
        reward = (self.max_reward * (motor_usage/576)) - ((motor_variation/576) * self.penalty_factor)
        self.prev_motors = motors
        return reward, False, False


    def teardown(self):
        pass
