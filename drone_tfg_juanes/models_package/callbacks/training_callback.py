from stable_baselines3.common.callbacks import BaseCallback


class TrainingCallback(BaseCallback):
    """Callback de entrenamiento para resetear y cerrar el entorno,
       evitando problemas de sincronización."""

    def __init__(self, env, verbose=1):
        super(TrainingCallback, self).__init__(verbose)
        self.env = env

    def _on_step(self) -> bool:
        return True

    def _on_rollout_start(self) -> None:
        pass#self.env.reset()

    def _on_training_end(self):
        print("Entrenamiento finalizado. Cerrando el entorno...")
        self.env.close()