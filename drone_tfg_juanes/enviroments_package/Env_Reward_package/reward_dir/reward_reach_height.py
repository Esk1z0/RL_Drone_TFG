from .reward_basic import RewardStrategyInterface


class RewardReachHeight(RewardStrategyInterface):

    @staticmethod
    def class_name():
        return "reach_height"

    def __init__(self, min_altitude=1, max_altitude=2, max_time=1):
        self.max_reward = 5
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.max_time = max_time
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
            reward = -1
            terminated = True
            finish = False

        return reward, terminated, finish

    def within_range(self, altitude):
        return self.min_altitude <= altitude <= self.max_altitude

    def timeout(self, time):
        return (time - self.start_time) >= self.max_time

    def teardown(self):
        pass
