from gymnasium.envs.registration import register
from enviroments_package.Drone_Env import DroneEnv
import gymnasium

register(
    id='drone_tfg_juanes/Drone-v01',
    entry_point="enviroments_package:Drone_Env",
    max_episode_steps=300,
)