import time

from drone_gymnasium_env.Drone_Env import DroneBaseEnv
from Utils.Quaternions import *


class Drone_TakeOff_ENV(DroneBaseEnv):
    """
    This environment meassure the height of the drone, with a minimum and a maximum height.
    Also, the drone must maintain a certain threshold of the original vector in order to assure the drone
    doesn't roll over.

    The reward() returns the exponential value of the time the drone maintains itself in the air.
    """

    def __init__(self, maxtime, command):
        super().__init__(maxtime, command)
        obs = super().get_obs()

        self.initial_altitude = obs["altimeter"]
        self.altitude_minimum = 5
        self.altitude_maximum = 7

        self.initial_quaternion = obs["imu"]
        self.quaternion_threshold = 30

        self.start = -1
        self.env_start_time = time.monotonic()

    def drone_turned_around(self, observation):
        q = observation["imu"]
        return angulo_entre_cuaterniones(self.initial_quaternion, q) > self.quaternion_threshold

    def drone_too_low(self, observation):
        return (self.start != -1) and (observation["altimeter"] <= (self.initial_altitude + self.altitude_minimum))

    def drone_too_high(self, observation):
        return (self.start != -1) and (observation["altimeter"] >= (self.initial_altitude + self.altitude_maximum))

    def timeout_env(self):
        return (time.monotonic() - self.env_start_time) > self.maxtime

    def terminated_situations(self, observation):
        return self.drone_too_low(observation) \
            or self.drone_too_high(observation) \
            or self.drone_turned_around(observation) \
            or self.timeout_env()

    def reward(self, observation):
        reward = 0
        terminated = self.terminated_situations(observation)
        if self.start == -1:
            if observation["altimeter"] > (self.initial_altitude + self.altitude_minimum):
                self.start = time.monotonic()
        else:
            reward = np.exp(time.monotonic() - self.start)
        return reward, terminated

    def reset(self, seed=None, options=None):
        obs = super().reset()
        self.initial_altitude = super().get_obs()["altimeter"]
        self.start = -1
        return obs


if __name__ == "__main__":
    pass
