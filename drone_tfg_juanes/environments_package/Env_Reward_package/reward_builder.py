import json
from .reward_runner import Reward_Runner
from .rewards import reward_dict


class RewardLoader:
    """This class fabricates the reward function used in the episode given the json configuration file"""
    def __init__(self, json_path):
        self.json_path = json_path
        self.current_package_index = -1
        self.packages = []

    def load_packages(self) -> None:
        """Reads the json file and get the reward curriculum with all
        the reward functions that will be used on trainning"""
        with open(self.json_path, 'r') as file:
            config = json.load(file)
        self.packages = config['reward_curriculum']

    def restart(self) -> None:
        """Restart the counter to get the first reward function without rereading the json file"""
        self.current_package_index = -1

    def get_next_reward_function(self) -> object:
        """Fabricates the current reward functions with all the test needed into a reward runner,
        if no more reward functions it returns None"""
        self.current_package_index = self.current_package_index + 1
        if self.current_package_index < len(self.packages):
            package = self.packages[self.current_package_index]
            return self._load_single_package(package["reward_function"])
        else:
            return None

    def _load_single_package(self, reward_function):
        """Loads a single reward function into a reward runner with its tests"""
        rewards = self._build_tests(reward_function["tests"])
        return Reward_Runner(
            name=reward_function["name"],
            info=reward_function["info"],
            max_time=reward_function["max_time"],
            final_reward=reward_function["final_reward"],
            command=reward_function["command"],
            rewards=rewards,
            last_function=self.current_package_index == (len(self.packages) - 1)
        )

    def _build_tests(self, tests):
        """It builds each test from a reward function one by one with its params defined on the configuration file"""
        tests_list = []
        for test in tests:
            class_constructor = reward_dict[test["name"]]
            class_params = test["parameters"]
            tests_list.append(class_constructor(**class_params))
        return tests_list
