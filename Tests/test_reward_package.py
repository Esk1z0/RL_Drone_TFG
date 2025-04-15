import unittest
import time
from drone_tfg_juanes.environments_package.Env_Reward_package.reward_builder import RewardLoader

json_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/environments_package/Env_Reward_package/reward_package_config/test_takeoff.json"
json_timer_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/environments_package/Env_Reward_package/reward_package_config/test_basic_reward.json"
json_zone_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/environments_package/Env_Reward_package/reward_package_config/test_zone.json"
json_height = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/environments_package/Env_Reward_package/reward_package_config/test_height.json"

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
        function = loader.get_next_reward_function()
        print(function.reward_command())

    def test_timer_reward(self):

        loader = RewardLoader(json_path)
        loader.load_packages()
        reward_timer_package = loader.get_next_reward_function()
        reward_timer_package.start_reward({})

        print(reward_timer_package.last_function)

        for _ in range(6):
            print(reward_timer_package._get_reward({}))
            time.sleep(2)

        self.assertEqual(True, True)

    def test_change_of_rewards(self):
        loader = RewardLoader(json_path)
        loader.load_packages()
        reward_package = loader.get_next_reward_function()
        reward_package.start_reward({})

        reward, terminated, change = 0, False, False

        while not terminated:
            while not change and not terminated:
                print(reward_package.last_function)
                reward, terminated, change = reward_package._get_reward({})
                print(reward, terminated, change)
                time.sleep(2)
            print("a")
            reward_package = loader.get_next_reward_function()
            reward_package.start_reward({})
            change = False
        self.assertEqual(True, True)

    def test_zone_reward(self):
        loader = RewardLoader(json_zone_path)
        loader.load_packages()
        reward_zone_package = loader.get_next_reward_function()
        reward_zone_package.start_reward({"gps": [0, 0, 0]})

        print(reward_zone_package._get_reward({"gps": [0.5, 0, 3]}))
        print(reward_zone_package._get_reward({"gps": [0, 0.7, 3]}))
        print(reward_zone_package._get_reward({"gps": [0.7, 0.7, 3]}))
        print(reward_zone_package._get_reward({"gps": [1, 0.7, 3]}))
        time.sleep(0.1)

        self.assertEqual(True, True)

    def test_reach_height(self):
        loader = RewardLoader(json_height)
        loader.load_packages()
        reward_zone_package = loader.get_next_reward_function()
        reward_zone_package.start_reward({"altimeter": 0.4})

        print(reward_zone_package._get_reward({"altimeter": 0.4}))
        print(reward_zone_package._get_reward({"altimeter": 2.1}))
        time.sleep(6)
        print(reward_zone_package._get_reward({"altimeter": 2.1}))
        time.sleep(0.1)
        print(reward_zone_package._get_reward({"altimeter": 2.1}))

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
