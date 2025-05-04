from gymnasium.envs.registration import register
from wrappers import *

register(
    id='tfg_juanes/CustomBioloid-v1',
    entry_point="environments_package.bioloid_env:BioloidEnv"
)