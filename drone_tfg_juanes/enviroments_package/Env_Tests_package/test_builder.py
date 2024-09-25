import json


class TestLoader:
    def __init__(self, json_path):
        self.json_path = json_path
        self.current_package_index = 0
        self.packages = []

    def load_packages(self):
        with open(self.json_path, 'r') as file:
            config = json.load(file)
        self.packages = config['test_packages']

    def get_next_package(self):
        self.current_package_index += 1
        if self.current_package_index < len(self.packages):
            package = self.packages[self.current_package_index]
            return [globals()[test['class_name']](test['params']) for test in package['tests']]
        return None

    def get_current_package_tests(self):
        package = self.packages[self.current_package_index]
        return [globals()[test['class_name']](test['params']) for test in package['tests']]