from time import perf_counter


class Reward_Runner:
    def __init__(self, name="", info="", alpha=0.99, final_reward=0, command=0, rewards=[]):
        self.rewards = rewards
        self.name = name
        self.info = info
        self.alpha = alpha
        self.command = command
        self.final_reward = final_reward

    def __str__(self):
        string = f"REWARD FUNCTION\nname: {self.name}\n" \
               f"info: {self.info}\n" \
               f"discount: {self.alpha}\n" \
               f"final_reward: {self.final_reward}\n" \
               f"command: {self.command}\n" \
               f"tests: "
        for reward in self.rewards:
            string += "\n-" + str(reward)
        return string

    def reward_command(self):
        return self.command

    def start_reward(self, obs: dict):
        start_time = perf_counter()
        for test in self.rewards:
            test.start_test(obs, start_time)

    def get_reward(self, obs) -> (int, bool, bool):
        #TODO: return the final reward when finished task
        actual_time = perf_counter()
        reward, terminated, finish_reward_function = 0, False, True
        for test in self.rewards:
            reward_aux, terminated_aux, finish_aux = test.get_reward(obs, actual_time)
            reward += reward_aux
            terminated = terminated_aux if terminated_aux else terminated
            finish_reward_function = finish_aux if not finish_aux else finish_reward_function
        if finish_reward_function and (reward == 0):
            reward = self.final_reward
        return reward, terminated, finish_reward_function
