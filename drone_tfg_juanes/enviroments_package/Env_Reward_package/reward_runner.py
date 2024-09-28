

class Reward_Runner:
    def __init__(self, name="dummy", info="NO INFO", alpha=0.99, final_reward=0, rewards=[]):
        self.rewards = rewards
        self.name = name
        self.info = info
        self.alpha = alpha
        self.final_reward = final_reward

    def __str__(self):
        string = f"REWARD FUNCTION\nname: {self.name}\n" \
               f"info: {self.info}\n" \
               f"discount: {self.alpha}\n" \
               f"final_reward: {self.final_reward}\n" \
               f"tests: "
        for reward in self.rewards:
            string += "\n-" + str(reward)
        return string



    def start_reward(self, data: dict):
        pass

    def get_reward(self):
        pass
