import os
import json

from stable_baselines3.common.logger import configure
from stable_baselines3.common.callbacks import CallbackList
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3 import PPO, A2C, DDPG, SAC, TD3
from sb3_contrib import RecurrentPPO, TRPO, TQC


from models_package.callbacks.custom_checkpoint_callback import CustomCheckpointCallback
from models_package.callbacks.training_callback import  TrainingCallback


class RLModelFactory:
    """
    Esta clase representa una fábrica abstracta para crear o cargar modelos de aprendizaje por refuerzo
    según los parámetros definidos en un archivo de configuración.

    Soporta algoritmos nativos de Stable-Baselines3 (SB3) y personalizados definidos dentro del sistema.
    """

    def __init__(self, config, env, base_dir) -> None:
        """
        Inicializa la fábrica con la configuración, el entorno y los directorios base.

        Args:
            config (TrainingConfig): Objeto de configuración con información del modelo, entorno y entrenamiento.
            env (gymnasium.Env): Entorno vectorizado para entrenamiento.
            base_dir (str): Ruta donde se almacenarán los logs, modelos y datos.
        """
        self.config = config
        self.env = env
        self.trained_so_far = 0
        self.available_algorithms = {
            "A2C": A2C,
            "TRPO": TRPO,
            "PPO": PPO,
            "RecurrentPPO": RecurrentPPO,
            "DDPG": DDPG,
            "TD3": TD3,
            "SAC": SAC,
            "TQC": TQC,
        }

        self._prepare_directories(base_dir)
        self._load_checkpoint()

    def _prepare_directories(self, base_dir) -> None:
        """
        Crea los directorios necesarios para guardar logs, modelos y datos, y define rutas internas.
        """
        self.log_dir = os.path.join(base_dir, "logs")
        self.data_dir = os.path.join(base_dir, "data_collected")
        self.model_dir = os.path.join(base_dir, "models")

        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)

        final_model = os.path.join(self.model_dir, "model_final.zip")
        default_model = os.path.join(self.model_dir, "model.zip")
        self.model_path = final_model if os.path.exists(final_model) else default_model

        self.checkpoint_path = os.path.join(self.model_dir, "checkpoint.json")

    def _load_checkpoint(self) -> None:
        """
        Carga el número de timesteps entrenados desde el checkpoint, o inicializa uno nuevo si no existe.
        """
        if os.path.exists(self.checkpoint_path) and os.path.exists(self.model_path):
            with open(self.checkpoint_path, "r") as f:
                data = json.load(f)
            self.trained_so_far = data.get("timesteps_trained", 0)
            print(f"[INFO] Checkpoint encontrado. Timesteps entrenados: {self.trained_so_far}")
        else:
            with open(self.checkpoint_path, "w") as f:
                json.dump({"timesteps_trained": 0}, f, indent=2)
            print("[INFO] No se encontró modelo. Entrenamiento desde cero.")

    def create_or_load_model(self) -> (BaseAlgorithm, CallbackList):
        algo_name = self.config.model_config.get("algorithm")
        policy = self.config.model_config.get("policy")
        params = self.config.model_config.get("params", {})

        model_class = self.available_algorithms.get(algo_name)
        if model_class is None:
            raise ValueError(f"[ERROR] Algoritmo no soportado: {algo_name}")

        if os.path.exists(self.model_path):
            print(f"[INFO] Cargando modelo desde {self.model_path}")
            model = model_class.load(self.model_path, env=self.env, verbose=1)
            logger = configure(self.log_dir, ["stdout", "csv"])
            model.set_logger(logger)
        else:
            print("[INFO] Creando nuevo modelo...")
            model = model_class(policy, self.env, verbose=1, **params)
            logger = configure(self.log_dir, ["stdout", "csv"])
            model.set_logger(logger)

        return model, self._get_callbacks()

    def get_trained_steps(self) -> int:
        """
        Devuelve la cantidad de timesteps ya entrenados según el checkpoint.

        Returns:
            int: Timesteps entrenados previamente.
        """
        return self.trained_so_far

    def _get_callbacks(self) -> CallbackList:
        """
        Crea y devuelve la lista de callbacks para el entrenamiento del modelo.

        Returns:
            CallbackList: Lista de callbacks a utilizar durante el entrenamiento.
        """
        callback_params = self.config.callback_config
        return CallbackList([
            TrainingCallback(env=self.env, verbose=1),
            CustomCheckpointCallback(
                log_dir=self.log_dir,
                data_collected_dir=self.data_dir,
                model_dir=self.model_dir,
                n_rollouts=callback_params.get("n_rollouts", 2048),
                last_checkpoint=self.get_trained_steps(),
                save_timestamp_every_n_steps=callback_params.get("save_timestamp_every_n_steps", 10000),
                verbose=callback_params.get("verbose", 1)
            )
        ])

