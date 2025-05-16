import os
import shutil
import json
from datetime import datetime
from stable_baselines3.common.callbacks import BaseCallback


def move_and_rename_csv(src_dir, dst_dir, new_name):
    """
    Copia el archivo 'progress.csv' desde src_dir a dst_dir con un nuevo nombre.

    Args:
        src_dir (str): Ruta de origen donde se encuentra 'progress.csv'.
        dst_dir (str): Ruta destino donde se copiará el archivo.
        new_name (str): Nombre del archivo de salida.
    """
    src_path = os.path.join(src_dir, 'progress.csv')
    dst_path = os.path.join(dst_dir, new_name)

    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"[CustomCheckpointCallback] Log copiado como: {dst_path}")
    else:
        print("[CustomCheckpointCallback] 'progress.csv' no encontrado.")


class CustomCheckpointCallback(BaseCallback):
    """
    Callback personalizado para guardar modelos, logs y checkpoint de timesteps periódicamente.

    Guarda:
    - El modelo principal ('model.zip' o 'case1_model.zip').
    - Un archivo CSV de progreso ('progress.csv') renombrado.
    - Un archivo JSON con los timesteps acumulados.
    - Un modelo adicional con timestamp, si ha pasado suficiente tiempo.

    Args:
        log_dir (str): Carpeta donde se generan los logs de entrenamiento (donde está 'progress.csv').
        data_collected_dir (str): Carpeta donde se guardarán las copias renombradas de los logs.
        model_dir (str): Carpeta donde se guardarán los modelos (.zip) y el archivo checkpoint (.json).
        n_steps (int): Número de rollouts tras los cuales se guardará un nuevo checkpoint.
        last_checkpoint (int): Número de timesteps ya entrenados (útil al continuar un entrenamiento anterior).
        save_timestamp_every_n_steps (int): Cada cuántos timesteps se guarda una copia adicional del modelo con timestamp.
        verbose (int): Nivel de verbosidad (0 = silencioso, 1 = imprime mensajes).
    """
    def __init__(self, log_dir, data_collected_dir, model_dir, n_rollouts,
                 last_checkpoint=0, save_timestamp_every_n_steps=10000, verbose=1):
        super().__init__(verbose)
        self.log_dir = log_dir
        self.data_collected_dir = data_collected_dir
        self.model_dir = model_dir
        self.n_rollouts = n_rollouts
        self.last_checkpoint_value = last_checkpoint
        self.save_timestamp_every_n_steps = save_timestamp_every_n_steps
        self.last_timestamp_checkpoint = (last_checkpoint // save_timestamp_every_n_steps) * save_timestamp_every_n_steps
        self.rollout_counter = 0
        self.num_timesteps_own = last_checkpoint

        self.checkpoint_file = os.path.join(model_dir, "checkpoint.json")
        self.data_collected_file = f"data_collected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    def _on_step(self) -> bool:
        self.num_timesteps_own += 1
        return True

    def _on_rollout_end(self) -> None:
        self.rollout_counter += 1
        if self.rollout_counter >= self.n_rollouts:
            self._save_checkpoint()
            self.rollout_counter = 0

    def _on_training_end(self) -> None:
        self._save_checkpoint(final=True)

    def _save_checkpoint(self, final=False) -> None:
        """Guarda modelo, logs y checkpoint acumulado."""
        self._copy_training_logs()
        self._save_model(final)
        self._update_checkpoint_file()
        self._maybe_save_model_with_timestamp()

    def _copy_training_logs(self) -> None:
        move_and_rename_csv(self.log_dir, self.data_collected_dir, self.data_collected_file)

    def _save_model(self, final=False) -> None:
        model_name = "model_final.zip" if final else "model.zip"
        model_path = os.path.join(self.model_dir, model_name)
        self.model.save(model_path)
        if self.verbose:
            print(f"[CustomCheckpointCallback] Modelo guardado en: {model_path}")

    def _maybe_save_model_with_timestamp(self) -> None:
        if (self.last_checkpoint_value - self.last_timestamp_checkpoint) >= self.save_timestamp_every_n_steps:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_path = os.path.join(self.model_dir, f"model_{timestamp}.zip")
            self.model.save(model_path)
            self.last_timestamp_checkpoint = self.last_checkpoint_value
            if self.verbose:
                print(f"[CustomCheckpointCallback] Modelo con timestamp guardado en: {model_path}")

    def _update_checkpoint_file(self) -> None:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.last_checkpoint_value = self.num_timesteps_own
        checkpoint_data = {
            "timesteps_trained": int(self.last_checkpoint_value),
            "last_save_time": timestamp_str
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)
