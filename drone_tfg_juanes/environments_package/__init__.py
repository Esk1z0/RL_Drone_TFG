from gymnasium.envs.registration import register
from environments_package.bioloid_env import Bioloid
import gymnasium
from .wrappers.remove_key_observation_wrapper import RemoveKeyObservationWrapper
from .wrappers.scale_action_wrapper import ScaleActionWrapper
from .wrappers.scale_reward_wrapper import ScaleRewardWrapper
from .wrappers.binary_action_wrapper import BinaryActionWrapper
from .callbacks.training_callback import TrainingCallback
from .callbacks.custom_checkpoint_callback import CustomCheckpointCallback

register(
    id='tfg_juanes/CustomBioloid-v1',
    entry_point="environments_package.bioloid_env:BioloidEnv"
)