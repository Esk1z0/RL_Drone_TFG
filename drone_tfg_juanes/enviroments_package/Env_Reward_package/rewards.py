from .reward_dir.reward_basic import RewardStrategyInterface
from .reward_dir.reward_no_roll import RewardNoRoll
from .reward_dir.reward_zone import RewardZone
from .reward_dir.reward_reach_height import RewardReachHeight
from .reward_dir.reward_timer import RewardTimer
from .reward_dir.reward_height import RewardHeight
from .reward_dir.reward_use_motors import RewardUseMotors

reward_dict = {
    str(RewardStrategyInterface.class_name()): RewardStrategyInterface,
    str(RewardNoRoll.class_name()): RewardNoRoll,
    str(RewardZone.class_name()): RewardZone,
    str(RewardReachHeight.class_name()): RewardReachHeight,
    str(RewardTimer.class_name()): RewardTimer,
    str(RewardHeight.class_name()): RewardHeight,
    str(RewardUseMotors.class_name()): RewardUseMotors
}
