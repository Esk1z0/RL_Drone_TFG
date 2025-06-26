from .reward_dir.reward_basic import RewardStrategyInterface
from .reward_dir.reward_no_roll import RewardNoRoll
from .reward_dir.reward_forward import RewardForwardDistance
from .reward_dir.reward_timer import RewardTimer

from .reward_dir.reward_use_motors import RewardUseMotors
from .reward_dir.reward_motor_penalty import RewardMotorInactivityPenalty
from .reward_dir.reward_no_roll_simplified import RewardNoRollSimplified
from .reward_dir.reward_forward_delta import RewardForwardDistanceDelta
from .reward_dir.reward_forward_with_penalty import RewardForwardWithPenalty
from .reward_dir.reward_stay_upright import RewardStayUpright
from .reward_dir.reward_position_debug import RewardPrintPosition

reward_dict = {
    str(RewardStrategyInterface.class_name()): RewardStrategyInterface,
    str(RewardNoRoll.class_name()): RewardNoRoll,
    str(RewardTimer.class_name()): RewardTimer,
    str(RewardUseMotors.class_name()): RewardUseMotors,
    str(RewardForwardDistance.class_name()): RewardForwardDistance,
    str(RewardMotorInactivityPenalty.class_name()): RewardMotorInactivityPenalty,
    str(RewardNoRollSimplified.class_name()): RewardNoRollSimplified,
    str(RewardForwardDistanceDelta.class_name()): RewardForwardDistanceDelta,
    str(RewardForwardWithPenalty.class_name()): RewardForwardWithPenalty,
    str(RewardStayUpright.class_name()): RewardStayUpright,
    str(RewardPrintPosition.class_name()): RewardPrintPosition
}
