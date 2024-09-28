import json
from .reward_runner import Reward_Runner
from .rewards import reward_dict


class RewardLoader:
    def __init__(self, json_path):
        self.json_path = json_path
        self.current_package_index = -1
        self.packages = []

    def load_packages(self):
        with open(self.json_path, 'r') as file:
            config = json.load(file)
        self.packages = config['reward_curriculum']

    def restart(self):
        self.current_package_index = -1

    def get_next_reward_function(self):
        self.current_package_index += 1
        if self.current_package_index < len(self.packages):
            package = self.packages[self.current_package_index]
            return self._load_single_package(package["reward_function"])
        else:
            return None

    def _load_single_package(self, reward_function):
        return Reward_Runner(
            name=reward_function["name"],
            info=reward_function["info"],
            alpha=reward_function["alpha"],
            final_reward=reward_function["final_reward"],
            command=reward_function["command"],
            rewards=self._build_tests(reward_function["tests"])
        )

    def _build_tests(self, tests):
        tests_list = []
        for test in tests:
            class_constructor = reward_dict[test["name"]]
            class_params = test["parameters"]
            tests_list.append(class_constructor(**class_params))
        return tests_list
