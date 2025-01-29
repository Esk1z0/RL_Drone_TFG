import os
import time

from enviroments_package.Drone_Env import DroneEnv
import numpy as np
import platform


world_dir = "./simulation_package/worlds/my_frst_webots_world.wbt"
env_config_dir = "./configs/reward_package_config/takeoff.json"


def three_instances():
    print(platform.system())
    print(os.listdir(os.getcwd()))
    ini = time.monotonic()

    # Crear tres instancias del entorno
    env = DroneEnv(world_dir, env_config_dir)
    env2 = DroneEnv(world_dir, env_config_dir)
    env3 = DroneEnv(world_dir, env_config_dir)
    ini2 = time.monotonic()

    # Resetear las tres instancias
    env.reset()
    env2.reset()
    env3.reset()

    action = np.array([50, 50, 50, 50])
    for i in range(20):
        # Realizar pasos en las tres instancias
        observation1, reward1, terminated1, truncated1, info1 = env.step(action)
        observation2, reward2, terminated2, truncated2, info2 = env2.step(action)
        observation3, reward3, terminated3, truncated3, info3 = env3.step(action)

        # Imprimir recompensas y observaciones
        print("env1:", reward1)
        print("env2:", reward2)
        print("env3:", reward3)
        print("obs1", observation1)

        # Verificar si alguna instancia ha terminado o necesita reiniciarse
        if terminated1 or truncated1:
            observation1, info1 = env.reset()
        if terminated2 or truncated2:
            observation2, info2 = env2.reset()
        if terminated3 or truncated3:
            observation3, info3 = env3.reset()

    fin_train = time.monotonic()

    # Cerrar las tres instancias
    env.close()
    env2.close()
    env3.close()

    time.sleep(3)
    fin = time.monotonic()

    print(f"tiempo train {fin_train - ini}")
    print(f"tiempo train sin crear webots {fin_train - ini2}")
    print(f"tiempo total {fin - ini}")


def two_instances():
    print(platform.system())
    print(os.listdir(os.getcwd()))
    ini = time.monotonic()
    env = DroneEnv(world_dir, env_config_dir)
    env2 = DroneEnv(world_dir, env_config_dir)
    ini2 = time.monotonic()

    env.reset()
    env2.reset()

    action = np.array([50, 50, 50, 50])
    for i in range(20):
        observation1, reward1, terminated1, truncated1, info = env.step(action)
        observation, reward2, terminated2, truncated2, info = env2.step(action)
        print("env1:", reward1)
        print("env2:", reward2)
        print("obs1", observation1)
        if terminated1 or truncated1 or terminated2 or truncated2:
            observation, info = env.reset()
            observation, info = env2.reset()
    fin_train = time.monotonic()
    env.close()
    env2.close()
    time.sleep(3)
    fin = time.monotonic()
    print(f"tiempo train {fin_train - ini}\ntiempo train sin crear webots {fin_train - ini2}\ntiempo total {fin - ini}")

def one_instance():
    print(platform.system())
    print(os.listdir(os.getcwd()))
    ini = time.monotonic()
    env = DroneEnv(world_dir, env_config_dir)
    ini2 = time.monotonic()
    env.reset()
    action = np.array([500, 500, 500, 500])
    for i in range(20):
        observation, reward, terminated, truncated, info = env.step(action)
        print(reward)
        if terminated or truncated:
            observation, info = env.reset()
    fin_train = time.monotonic()
    env.close()
    time.sleep(3)
    fin = time.monotonic()
    print(f"tiempo train {fin_train-ini}\ntiempo train sin crear webots {fin_train-ini2}\ntiempo total {fin-ini}")

def vecenv_func():
    pass

if __name__ == "__main__":
    three_instances()

