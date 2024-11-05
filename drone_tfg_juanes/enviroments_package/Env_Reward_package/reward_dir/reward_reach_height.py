from .reward_basic import RewardStrategyInterface
import math


class RewardReachHeight(RewardStrategyInterface):

    @staticmethod
    def class_name():
        return "reach_height"

    def __init__(self, min_altitude=1, max_altitude=2, max_time=1, decay_rate=0.1, max_reward=1):
        self.max_reward = max_reward
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.max_time = max_time
        self.decay_rate = decay_rate
        self.start_time = -1

    def __str__(self):
        string = "name: Reach Height" \
                 "\ndescription: It measures that the drone reach a certain " \
                 "height and stays there for a certain time before ending the training"
        return string

    def start_test(self, obs: dict, time) -> None:
        pass

    def get_reward(self, obs: dict, time) -> (int, bool, bool):
        altitude = obs["altimeter"]
        in_range = self.within_range(altitude)
        reward, terminated, finish = 0, False, False

        if in_range:
            reward = self.max_reward
            if self.start_time == -1:
                self.start_time = time
            else:
                if self.timeout(time):
                    terminated = True
                    finish = True
        elif self.start_time != -1:
            reward = self.calculate_reward_out_of_range(altitude)
            terminated = True
            finish = False

        return reward, terminated, finish

    def within_range(self, altitude):
        return self.min_altitude <= altitude <= self.max_altitude

    def timeout(self, time):
        return (time - self.start_time) >= self.max_time

    def teardown(self):
        pass

    def calculate_reward_out_of_range(self, altitude):

        distance = abs(altitude - ((self.max_altitude+self.min_altitude)/2))

        # Calcular la recompensa usando una función exponencial inversa
        reward = self.max_reward * math.exp(-self.decay_rate * distance)

        return reward
