from gymnasium.envs.registration import register
from environments_package.Bioloid_Env import Bioloid
import gymnasium
from .Wrappers.RemoveKeyObservationWrapper import RemoveKeyObservationWrapper
from .Wrappers.ScaleActionWrapper import ScaleActionWrapper
from .Wrappers.ScaleRewardWrapper import ScaleRewardWrapper
from .Wrappers.BinaryActionWrapper import BinaryActionWrapper
from .Callbacks.TrainingCallback import TrainingCallback
from .Callbacks.CustomCcheckpointCallback import CustomCheckpointCallback

register(
    id='tfg_juanes/CustomBioloid-v1',
    entry_point="environments_package.Bioloid_Env:BioloidEnv"
)