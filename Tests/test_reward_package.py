import unittest
import time
from drone_tfg_juanes.enviroments_package.Env_Reward_package.reward_builder import RewardLoader

json_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/enviroments_package/Env_Reward_package/reward_package_config/test_takeoff.json"

json_timer_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/enviroments_package/Env_Reward_package/reward_package_config/test_basic_reward.json"

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


    def test_basic_reward_load(self):
        loader = RewardLoader(json_path)
        loader.load_packages()
        print(loader.packages)
        self.assertEqual(True, True)

    def test_load_takeoff_build(self):
        loader = RewardLoader(json_path)
        loader.load_packages()
        print(loader.get_next_reward_function())
        self.assertEqual(True, True)

    def test_info_reward_runner(self):
        loader = RewardLoader(json_path)
        loader.load_packages()
        print(loader.get_next_reward_function().reward_command())

    def test_timer_reward(self):

        loader = RewardLoader(json_timer_path)
        loader.load_packages()
        reward_timer_package = loader.get_next_reward_function()
        reward_timer_package.start_reward({})

        for _ in range(6):
            print(reward_timer_package.get_reward({}))
            time.sleep(1)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
