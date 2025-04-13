import os
import shutil
import json
from datetime import datetime
from stable_baselines3.common.callbacks import BaseCallback

def move_and_rename_csv(src_dir, dst_dir, new_name):
    """
    Busca 'progress.csv' en src_dir y lo copia/renombra a dst_dir/new_name.
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
    Callback que guarda el modelo, actualiza los logs y un checkpoint de entrenamiento
    después de cada rollout.
      - Guarda el modelo en el directorio de modelos.
      - Actualiza el archivo de logs en el directorio data_collected, utilizando un nombre
        que incluye la fecha y hora (fijado al inicio del entrenamiento).
      - Actualiza el checkpoint en un archivo JSON, acumulando solo los incrementos de timesteps
        desde el último guardado.
    """
    def __init__(self, log_dir, data_collected_dir, model_dir, n_steps, last_checkpoint=0,verbose=1):
        """
        :param log_dir: Directorio donde se guardan los logs.
        :param data_collected_dir: Directorio donde se guarda el archivo de logs acumulativos.
        :param model_dir: Directorio donde se guardan los modelos y el checkpoint.
        :param verbose: Nivel de detalle de impresión.
        """
        super().__init__(verbose)
        self.log_dir = log_dir
        self.data_collected_dir = data_collected_dir
        self.model_dir = model_dir

        # Archivo de checkpoint (se asume que model_dir existe)
        self.checkpoint_file = os.path.join(model_dir, "checkpoint.json")

        # Fijar un nombre único para el archivo de logs acumulativos, con fecha y hora
        self.data_collected_file = f"data_collected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # Inicializar variable interna para el valor en el último checkpoint
        self.last_checkpoint_value = last_checkpoint
        self.n_steps = n_steps

    def _on_step(self) -> bool:
        return True

    def _on_rollout_end(self) -> None:
        """Se ejecuta al inicio de cada rollout (cuando se generan nuevos logs)."""
        self._save_checkpoint()

    def _on_training_end(self) -> None:
        """Se ejecuta al finalizar el entrenamiento para guardar el último estado."""
        self._save_checkpoint(final=True)

    def _save_checkpoint(self, final=False) -> None:
        """
        Guarda el modelo, actualiza el archivo de logs y almacena un archivo JSON
        con el número acumulado de timesteps entrenados. Se suma la diferencia de timesteps
        (delta) desde la última actualización para evitar duplicados.
        """
        # Actualizar logs: copiar el progress.csv al archivo único, cuyo nombre se ha fijado en __init__
        move_and_rename_csv(
            self.log_dir,
            self.data_collected_dir,
            self.data_collected_file
        )

        # Obtener el valor actual de timesteps

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Guardar modelo con un nombre (si final, "model_final.zip"; de lo contrario, "model.zip")
        model_name = "model_final.zip" if final else "model.zip"
        model_path = os.path.join(self.model_dir, model_name)
        self.model.save(model_path)
        if self.verbose > 0:
            print(f"[CustomCheckpointCallback] Modelo guardado en: {model_path}")

        # Leer el valor previo de los timesteps desde el checkpoint
        previous_total = 0
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r") as f:
                    checkpoint_data = json.load(f)
                    previous_total = checkpoint_data.get("timesteps_trained", 0)
            except Exception as e:
                print(f"[WARNING] No se pudo leer el JSON, reiniciando los timesteps: {e}")
                previous_total = 0

        self.last_checkpoint_value += self.n_steps

        # Guardar el nuevo checkpoint
        checkpoint_data = {
            "timesteps_trained": int(self.last_checkpoint_value),
            "last_save_time": timestamp_str
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)
