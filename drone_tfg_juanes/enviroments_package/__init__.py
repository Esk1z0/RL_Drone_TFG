from gymnasium.envs.registration import register
from enviroments_package.Drone_Env import DroneEnv
import gymnasium
from .Wrappers.RemoveKeyObservationWrapper import RemoveKeyObservationWrapper
from .Wrappers.ScaleActionWrapper import ScaleActionWrapper
from .Wrappers.ScaleRewardWrapper import ScaleRewardWrapper
from .Wrappers.BinaryActionWrapper import BinaryActionWrapper

register(
    id='drone_tfg_juanes/Drone-v1',
    entry_point="enviroments_package.Drone_Env:DroneEnv",
    max_episode_steps=300,
)