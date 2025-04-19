from .reward_dir.reward_basic import RewardStrategyInterface
from .reward_dir.reward_no_roll import RewardNoRoll
from .reward_dir.reward_forward import RewardForwardDistance
from .reward_dir.reward_timer import RewardTimer

from .reward_dir.reward_use_motors import RewardUseMotors
from .reward_dir.reward_motor_penalty import RewardMotorInactivityPenalty

reward_dict = {
    str(RewardStrategyInterface.class_name()): RewardStrategyInterface,
    str(RewardNoRoll.class_name()): RewardNoRoll,
    str(RewardTimer.class_name()): RewardTimer,
    str(RewardUseMotors.class_name()): RewardUseMotors,
    str(RewardForwardDistance.class_name()): RewardForwardDistance,
    str(RewardMotorInactivityPenalty.class_name()): RewardMotorInactivityPenalty
}
