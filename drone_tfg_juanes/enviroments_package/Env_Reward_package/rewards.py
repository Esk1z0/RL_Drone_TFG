from .reward_dir.reward_basic import RewardStrategyInterface
from .reward_dir.reward_no_roll import RewardNoRoll
from .reward_dir.reward_timer import RewardTimer


reward_dict = {
    str(RewardStrategyInterface.class_name()): RewardStrategyInterface,
    str(RewardNoRoll.class_name()): RewardNoRoll,
    str(RewardTimer.class_name()): RewardTimer
}
