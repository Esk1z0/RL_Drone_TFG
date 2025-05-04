import json


class TrainingConfig:
    def __init__(self, config_json):
        self.config = config_json
        self.env_config = config_json.get("env", {})
        self.model_config = config_json.get("model", {})
        self.train_config = config_json.get("training", {})
        self.callback_config = config_json.get("callback", {})


class TrainingConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path

    def load(self) -> TrainingConfig:
        with open(self.config_path, "r") as f:
            data = json.load(f)
        return TrainingConfig(data)
