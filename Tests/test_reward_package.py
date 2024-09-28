import unittest
import time
from drone_tfg_juanes.enviroments_package.Env_Reward_package.reward_builder import RewardLoader

json_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/enviroments_package/Env_Reward_package/reward_package_config/test_takeoff.json"

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
        print(loader.get_current_reward_function())
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
