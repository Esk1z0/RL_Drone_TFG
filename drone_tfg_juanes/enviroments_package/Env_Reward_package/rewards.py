from .reward_dir.reward_basic import RewardStrategyInterface
from .reward_dir.reward_no_roll import RewardNoRoll

reward_dict = {
    str(RewardStrategyInterface.class_name()): RewardStrategyInterface,
    str(RewardNoRoll.class_name()): RewardNoRoll
}
