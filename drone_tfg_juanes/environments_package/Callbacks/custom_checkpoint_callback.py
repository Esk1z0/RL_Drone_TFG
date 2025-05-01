import os
import shutil
import json
from datetime import datetime
from stable_baselines3.common.callbacks import BaseCallback


def move_and_rename_csv(src_dir, dst_dir, new_name):
    """Copia el archivo 'progress.csv' desde src_dir a dst_dir renombrado como new_name."""
    src_path = os.path.join(src_dir, 'progress.csv')
    dst_path = os.path.join(dst_dir, new_name)

    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"[CustomCheckpointCallback] Log copiado como: {dst_path}")
    else:
        print("[CustomCheckpointCallback] 'progress.csv' no encontrado.")


class CustomCheckpointCallback(BaseCallback):
    """
    Callback que guarda el modelo, logs y checkpoint JSON tras acumular 'n_steps'.
    También guarda un modelo adicional con timestamp cada 'save_timestamp_every_n_steps'.

    Compatible con PPO, SAC, TD3, etc.
    """
    def __init__(self, log_dir, data_collected_dir, model_dir, n_steps,
                 last_checkpoint=0, save_timestamp_every_n_steps=10000, verbose=1):
        super().__init__(verbose)
        self.log_dir = log_dir
        self.data_collected_dir = data_collected_dir
        self.model_dir = model_dir
        self.n_steps = n_steps
        self.last_checkpoint_value = last_checkpoint
        self.save_timestamp_every_n_steps = save_timestamp_every_n_steps
        self.last_timestamp_checkpoint = last_checkpoint
        self.step_counter = 0

        self.checkpoint_file = os.path.join(model_dir, "checkpoint.json")
        self.data_collected_file = f"data_collected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    def _on_step(self) -> bool:
        self.step_counter += 1

        if self.step_counter >= self.n_steps:
            self._save_checkpoint()
            self.step_counter = 0

        return True

    def _on_training_end(self) -> None:
        self._save_checkpoint(final=True)

    def _save_checkpoint(self, final=False) -> None:
        """Guarda modelo, log y checkpoint acumulado."""
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
        self.last_checkpoint_value += self.n_steps
        checkpoint_data = {
            "timesteps_trained": int(self.last_checkpoint_value),
            "last_save_time": timestamp_str
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)
