import os
import shutil
import json
from datetime import datetime
from stable_baselines3.common.callbacks import BaseCallback


def move_and_rename_csv(src_dir, dst_dir, new_name):
    """
    Busca el archivo 'progress.csv' en el directorio de origen y lo copia al directorio de destino
    con un nuevo nombre especificado.

    Args:
        src_dir (str): Ruta del directorio de origen que contiene 'progress.csv'.
        dst_dir (str): Ruta del directorio de destino donde se guardará el archivo.
        new_name (str): Nuevo nombre con el que se guardará el archivo en el destino.
    """
    csv_file = 'progress.csv'
    src_path = os.path.join(src_dir, csv_file)

    if not os.path.exists(src_path):
        print("No se encontró el archivo 'progress.csv' en el directorio de origen.")
        return

    dst_path = os.path.join(dst_dir, new_name)
    shutil.copy2(src_path, dst_path)
    print(f"Archivo copiado y renombrado a {dst_path}")


class CustomCheckpointCallback(BaseCallback):
    """
    Callback personalizado para gestionar checkpoints y registro de logs durante el entrenamiento.

    Funcionalidades:
    - Guarda el modelo tras cada rollout (en model.zip)
    - Cada N rollouts, guarda una copia adicional con fecha y hora.
    - Copia el archivo de progreso ('progress.csv') renombrado por fecha.
    - Actualiza un checkpoint con los timesteps entrenados acumulados.

    Args:
        log_dir (str): Directorio de salida de logs generados por el modelo.
        data_collected_dir (str): Directorio donde se guardan los logs renombrados por fecha.
        model_dir (str): Directorio donde se guarda el modelo y el checkpoint.
        n_steps (int): Número de pasos por cada rollout.
        last_checkpoint (int): Número de timesteps ya entrenados (para continuar entrenamiento).
        save_every_n_rollouts (int): Cada cuántos rollouts guardar una copia con timestamp.
        verbose (int): Nivel de detalle en las salidas por consola.
    """

    def __init__(self, log_dir, data_collected_dir, model_dir, n_steps,
                 last_checkpoint=0, save_every_n_rollouts=10, verbose=1) -> None:
        super().__init__(verbose)
        self.log_dir = log_dir
        self.data_collected_dir = data_collected_dir
        self.model_dir = model_dir
        self.n_steps = n_steps
        self.last_checkpoint_value = last_checkpoint
        self.save_every_n_rollouts = save_every_n_rollouts
        self.rollout_count = 0

        self.checkpoint_file = os.path.join(model_dir, "checkpoint.json")
        self.data_collected_file = f"data_collected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    def _on_step(self) -> bool:
        return True

    def _on_rollout_end(self) -> None:
        self.rollout_count += 1
        self._save_checkpoint()

        # Guardar modelo adicional con timestamp cada N rollouts
        if self.rollout_count % self.save_every_n_rollouts == 0:
            self._save_model_with_timestamp()

    def _on_training_end(self) -> None:
        self._save_checkpoint(final=True)

    def _save_checkpoint(self, final=False) -> None:
        self._copy_training_logs()
        self._save_model(final)
        self._update_checkpoint_file()

    def _copy_training_logs(self) -> None:
        move_and_rename_csv(
            self.log_dir,
            self.data_collected_dir,
            self.data_collected_file
        )

    def _save_model(self, final=False) -> None:
        model_name = "model_final.zip" if final else "model.zip"
        model_path = os.path.join(self.model_dir, model_name)
        self.model.save(model_path)
        if self.verbose > 0:
            print(f"[CustomCheckpointCallback] Modelo guardado en: {model_path}")

    def _save_model_with_timestamp(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = os.path.join(self.model_dir, f"model_{timestamp}.zip")
        self.model.save(model_path)
        if self.verbose > 0:
            print(f"[CustomCheckpointCallback] Modelo adicional guardado en: {model_path}")

    def _update_checkpoint_file(self) -> None:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        previous_total = 0
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r") as f:
                    checkpoint_data = json.load(f)
                    previous_total = checkpoint_data.get("timesteps_trained", 0)
            except Exception as e:
                print(f"[WARNING] No se pudo leer el JSON, reiniciando los timesteps: {e}")

        self.last_checkpoint_value += self.n_steps

        checkpoint_data = {
            "timesteps_trained": int(self.last_checkpoint_value),
            "last_save_time": timestamp_str
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)
