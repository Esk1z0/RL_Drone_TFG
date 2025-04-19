import gymnasium


class ScaleRewardWrapper(gymnasium.RewardWrapper):
    def __init__(self, env, scale_factor=1.0):
        super().__init__(env)
        # Definir un factor de escala
        self.scale_factor = scale_factor

    def reward(self, reward):
        # Escalar la recompensa según el factor de escala
        return reward * self.scale_factor
