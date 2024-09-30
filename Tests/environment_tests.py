import unittest
import time
from drone_tfg_juanes.enviroments_package.Drone_Env import DroneEnv

world_dir = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/simulation_package/worlds/my_frst_webots_world.wbt"
json_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/enviroments_package/Env_Reward_package/reward_package_config/test_takeoff.json"


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_setup_close(self):
        try:
            env = DroneEnv(world_dir, json_path)
            time.sleep(7)
            env.close()
        except Exception as e:
            print(e)
            assert False
        assert True

    def test_get_observation_action_space(self):
        env = DroneEnv(world_dir, json_path)
        print(env.observation_space)
        print(env.action_space)
        env.close()

    def test_action_sample(self):
        env = DroneEnv(world_dir, json_path)
        x = env.action_space.sample()
        print(type(x))
        env.close()

    def test_one_step(self):
        env = DroneEnv(world_dir, json_path)
        env.reset()
        env.step(action=env.action_space.sample())
        time.sleep(5)
        env.close()
        assert (True, True)


    def test_100step_cycle(self):
        env = DroneEnv(world_dir, json_path)
        observation = env.reset()
        action = [100, 100, 100]
        for i in range(100):
            action = env.action_space.sample() if i%20 == 0 else action
            observation, reward, terminated, truncated, info = env.step(action)
            print(observation)
            if terminated or truncated:
                observation, info = env.reset()

        env.close()

    def test_reward_function(self):
        pass


if __name__ == '__main__':
    unittest.main()
