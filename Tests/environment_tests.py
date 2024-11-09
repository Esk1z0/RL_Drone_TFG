import unittest
import time

import numpy as np

from drone_tfg_juanes.enviroments_package.Drone_Env import DroneEnv
from drone_tfg_juanes.enviroments_package.Wrappers.RemoveKeyObservationWrapper import RemoveKeyObservationWrapper
from drone_tfg_juanes.enviroments_package.Wrappers.ScaleActionWrapper import ScaleActionWrapper
from drone_tfg_juanes.enviroments_package.Wrappers.ScaleRewardWrapper import ScaleRewardWrapper

world_dir = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/simulation_package/worlds/my_frst_webots_world.wbt"
json_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/configs/reward_package_config/test_takeoff.json"
json_zone_no_roll_path = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/configs/reward_package_config/test_zone_no_roll.json"
json_take_off = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/configs/reward_package_config/takeoff.json"


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
        print(env.step(action=env.action_space.sample()))
        time.sleep(5)
        env.close()
        assert (True, True)

    def test_two_step_observation(self):
        env = DroneEnv(world_dir, json_path)
        env.reset()
        observation, reward, terminated, truncated, info = env.step(action=env.action_space.sample())
        print(observation["altimeter"])
        time.sleep(5)
        observation, reward, terminated, truncated, info = env.step(action=env.action_space.sample())
        print(observation["altimeter"])
        env.close()
        assert (True, True)

    def test_100step_cycle(self):
        env = DroneEnv(world_dir, json_path)
        observation = env.reset()
        action = [100, 100, 100, 100]
        print(observation)
        for i in range(100):
            action = env.action_space.sample() if i % 20 == 0 else action
            observation, reward, terminated, truncated, info = env.step(action)

            if terminated or truncated:
                observation, info = env.reset()

        env.close()

    def test_reward_function(self):
        env = DroneEnv(world_dir, json_path)
        env.reset()
        action = [100, 100, 100, 100]
        for i in range(150):
            action = env.action_space.sample() if i % 20 == 0 else action
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward, terminated)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()

    def test_two_reward_functions(self):
        env = DroneEnv(world_dir, json_zone_no_roll_path)
        env.reset()
        action = [100, 100, 100, 100]
        for i in range(150):
            action = env.action_space.sample() if i % 20 == 0 else action
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward, terminated)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()

    def test_nada(self):
        env = DroneEnv(world_dir, json_path)
        env.reset()
        action = np.array([500, 500, 500, 500])
        for i in range(50):
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()

    def test_takeoff(self):
        env = DroneEnv(world_dir, json_take_off, no_render=False)
        env.reset()

        for i in range(100):
            action = np.random.rand(4) * 500
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()


    def test_takeoff_sequence(self):
        env = DroneEnv(world_dir, json_take_off, no_render=False)
        env.reset()

        for i in range(10):
            action = np.random.rand(4) * 500
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()
        time.sleep(0.1)
        env.reset()

        for i in range(10):
            action = np.random.rand(4) * 500
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()


    def test_observation_wrapper(self):
        env = DroneEnv(world_dir, json_take_off, no_render=True)
        env = RemoveKeyObservationWrapper(env, remove_keys=["camera", "gps"])
        env.reset()

        for i in range(10):
            action = np.random.rand(4) * 500
            observation, reward, terminated, truncated, info = env.step(action)
            print(observation)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()

    def test_action_wrapper(self):
        env = DroneEnv(world_dir, json_take_off, no_render=True)
        env = ScaleActionWrapper(env, in_low=0, in_high=2, out_low=0, out_high=576)
        env.reset()

        for i in range(10):
            action = np.random.rand(4)
            print(action)
            observation, reward, terminated, truncated, info = env.step(action)
            print(observation)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()

    def test_reward_wrapper(self):
        env = DroneEnv(world_dir, json_take_off, no_render=False)
        env = ScaleRewardWrapper(env, scale_factor=0.1)
        env.reset()

        for i in range(10):
            action = np.random.rand(4) * 500
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward)
            if terminated :
                observation, info = env.reset()
        env.close()

    def test_all_wrappers(self):
        env = DroneEnv(world_dir, json_take_off, no_render=True)
        env = ScaleActionWrapper(env, in_low=0, in_high=2, out_low=0, out_high=576)
        env = RemoveKeyObservationWrapper(env, remove_keys=["camera", "gps"])
        env = ScaleRewardWrapper(env, scale_factor=0.1)
        env.reset()

        for i in range(10):
            action = np.random.rand(4)
            print(action)
            observation, reward, terminated, truncated, info = env.step(action)
            print(observation)
            print(reward)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()

    def test_vec_env(self):
        from stable_baselines3.common.vec_env import DummyVecEnv

        def make_env():
            return DroneEnv(world_dir, json_take_off, no_render=True)

        num_envs = 4  # Número de entornos en paralelo
        env = DummyVecEnv([make_env]*num_envs)

        # Resetea el entorno vectorizado
        observations = env.reset()

        # Ciclo para probar el entorno con reset y step
        for _ in range(10):  # Cambia el número de iteraciones según lo necesites
            # Genera acciones aleatorias para cada entorno en paralelo
            actions = np.array([env.action_space.sample() for _ in range(num_envs)])

            observations, rewards, dones, infos = env.step(actions)
            print("Observaciones:", observations)
            print("Recompensas:", rewards)
            print("Terminado:", dones)
            print("Infos:", infos)

            # Resetea solo los entornos que hayan terminado
            if any(dones):
                observations = env.reset()  # Esto reinicia solo los entornos terminados

            # Puedes agregar una pausa si es necesario para observar los cambios
            time.sleep(0.1)

        # Cierra el entorno al terminar
        env.close()

    def test_basicReward(self):
        json_basic = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/configs/reward_package_config/basic_no_roll.json"
        env = DroneEnv(world_dir, json_basic, no_render=False)
        env.reset()

        for i in range(100):
            action = np.random.rand(4) * 500
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward, terminated, truncated)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()


    def test_timeout_rerun(self):
        from drone_tfg_juanes.simulation_package.controllers.xyz_controller.drone_library.config import TIME_OUT
        json_basic = "/Users/jeste/Desktop/Clase/TFG/drone_tfg_juanes/configs/reward_package_config/basic_no_roll.json"
        env = DroneEnv(world_dir, json_basic, no_render=False)
        env.reset()

        time.sleep(TIME_OUT+15)
        print(env.drone.is_sim_out())
        env.reset()
        for i in range(100):
            action = np.random.rand(4) * 500
            observation, reward, terminated, truncated, info = env.step(action)
            print(reward, terminated, truncated)
            if terminated or truncated:
                observation, info = env.reset()
        env.close()


if __name__ == '__main__':
    unittest.main()
