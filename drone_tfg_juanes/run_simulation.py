from enviroments_package.Drone_Env import DroneEnv
import numpy as np


world_dir = "./simulation_package/worlds/my_frst_webots_world.wbt"
env_config_dir = "./configs/reward_package_config/takeoff.json"

if __name__ == "__main__":

    env = DroneEnv(world_dir, env_config_dir)
    env.reset()
    action = np.array([500, 500, 500, 500])
    for i in range(20):
        observation, reward, terminated, truncated, info = env.step(action)
        print(reward)
        if terminated or truncated:
            observation, info = env.reset()
    env.close()
