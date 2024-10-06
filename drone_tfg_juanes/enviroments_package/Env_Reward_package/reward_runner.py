from time import perf_counter


class Reward_Runner:
    def __init__(self, name="", info="", max_time=1, final_reward=0, command=0, rewards=[], last_function=False):
        self.rewards = rewards
        self.name = name
        self.info = info
        self.max_time = max_time
        self.command = command
        self.final_reward = final_reward
        self.last_function = last_function
        self.start_time = 0

    def __str__(self):
        string = f"REWARD FUNCTION\nname: {self.name}\n" \
                 f"info: {self.info}\n" \
                 f"max_time: {self.max_time}\n" \
                 f"final_reward: {self.final_reward}\n" \
                 f"command: {self.command}\n" \
                 f"tests: "
        for reward in self.rewards:
            string += "\n-" + str(reward)
        return string

    def reward_command(self):
        return self.command

    def start_reward(self, obs: dict):
        self.start_time = perf_counter()
        for test in self.rewards:
            test.start_test(obs, self.start_time)

    def get_reward(self, obs) -> (int, bool, bool):
        reward, terminated, finish_reward_function = 0, False, True
        actual_time = perf_counter()

        for test in self.rewards:
            reward_aux, terminated_aux, finish_aux = test.get_reward(obs, actual_time)
            reward += reward_aux
            terminated = terminated_aux if terminated_aux else terminated
            finish_reward_function = finish_aux if not finish_aux else finish_reward_function

        if self._time_out(actual_time):
            terminated = True
            reward = self.final_reward if finish_reward_function else 0
        elif finish_reward_function and self.last_function:
            terminated = True
            reward = self.final_reward

        return reward, terminated, finish_reward_function

    def _time_out(self, time):
        return self.max_time <= (time - self.start_time)
