import unittest
import time
from drone_tfg_juanes.enviroments_package.Drone_Env import DroneEnv

world_dir = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/simulation_package/worlds/my_frst_webots_world.wbt"

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_setup_close(self):
        try:
            env = DroneEnv(world_dir)
            time.sleep(5)
            env.close()
        except Exception as e:
            print(e)
            assert False
        assert True

    def test_get_observation_action_space(self):
        env = DroneEnv(world_dir)
        print(env.observation_space)
        print(env.action_space)
        env.close()


if __name__ == '__main__':
    unittest.main()
