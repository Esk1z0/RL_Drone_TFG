import unittest
import time

import numpy as np

from drone_tfg_juanes.environments_package.Bioloid_Env import BioloidEnv
from drone_tfg_juanes.environments_package.Wrappers.RemoveKeyObservationWrapper import RemoveKeyObservationWrapper
from drone_tfg_juanes.environments_package.Wrappers.ScaleActionWrapper import ScaleActionWrapper
from drone_tfg_juanes.environments_package.Wrappers.ScaleRewardWrapper import ScaleRewardWrapper

world_dir = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/simulation_package/worlds/bioloid_env.wbt"
json_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/configs/reward_package_config/test_bioloid.json"



class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_100step_cycle(self):
        env = BioloidEnv(world_dir, json_path, no_render=False)
        observation = env.reset()
        action = [0] * 16
        print(observation)
        for i in range(100):
            action = env.action_space.sample() if i % 20 == 0 else action
            observation, reward, terminated, truncated, info = env.step(action)
            #print("reward:", reward)
            #print(action)
            #print(observation)
            if terminated or truncated:
                observation, info = env.reset()

        env.close()

    def test_reward_function(self):
        env = BioloidEnv(world_dir, json_path)
        env.reset()
        action = [100, 100, 100, 100]
        for i in range(150):
            action = env.action_space.sample() if i % 20 == 0 else action
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward, terminated)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()



if __name__ == '__main__':
    unittest.main()
