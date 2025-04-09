from stable_baselines3.common.callbacks import BaseCallback
import os
import shutil
from datetime import datetime
import json

def update_model(model, env, log_dir='./logs/', n_eval_episodes=10):
    """
    Evalúa el modelo y actualiza el archivo de evaluación en CSV si la recompensa es la mejor hasta el momento.
    Retorna True si mejora la recompensa máxima, False en caso contrario.
    """
    eval_file_path = os.path.join(log_dir, "evaluate.csv")

    # Asegurarse de que existe la carpeta y el archivo
    os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(eval_file_path):
        pd.DataFrame(columns=["reward", "timestamp"]).to_csv(eval_file_path, index=False)

    eval_df = pd.read_csv(eval_file_path)
    max_reward = eval_df["reward"].max() if not eval_df.empty else float('-inf')

    mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, return_episode_rewards=False)

    if mean_reward > max_reward:
        new_row = pd.DataFrame({
            "reward": [mean_reward],
            "timestamp": [datetime.now().strftime("%Y%m%d_%H%M%S")]
        })
        new_row.to_csv(eval_file_path, mode='a', header=False, index=False)
        env.close()
        return True
    else:
        env.close()
        return False

def move_and_rename_csv(src_dir, dst_dir, new_name):
    """
    Busca 'progress.csv' en 'src_dir' y lo copia/renombra a 'dst_dir/new_name'.
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
    Callback que guarda el modelo, logs y un checkpoint de entrenamiento después de cada rollout.
    - Guarda el modelo en "ruta_base/modelos/"
    - Guarda los logs en "ruta_base/logs/"
    - Guarda el número de timesteps entrenados en "ruta_base/checkpoint.json"
    """

    def __init__(self, log_dir, data_collected_dir, model_dir, verbose=1):
        """
        :param base_path: Ruta base donde se guardarán todos los archivos.
        :param model_prefix: Prefijo del modelo guardado.
        :param verbose: Nivel de detalle de impresión.
        """
        super().__init__(verbose)
        self.log_dir = log_dir
        self.data_collected_dir = data_collected_dir
        self.model_dir = model_dir

        # Archivo de checkpoint
        self.checkpoint_file = os.path.join(model_dir, "checkpoint.json")

        # Archivo de Datos
        self.data_collected_file = os.path.join(data_collected_dir, f'data_collected_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

    def _on_step(self) -> bool:
        return True

    def _on_rollout_end(self) -> None:
        """Se ejecuta al final de cada rollout (cuando se generan nuevos logs)."""
        self._save_checkpoint()

    def _on_training_end(self) -> None:
        """Se ejecuta al finalizar el entrenamiento para guardar el último estado."""
        self._save_checkpoint(final=True)

    def _save_checkpoint(self, final=False) -> None:
        """
        Guarda el modelo, copia/renombra el progress.csv y almacena un archivo JSON con los timesteps entrenados.
        """

        move_and_rename_csv(
            self.log_dir,
            self.data_collected_dir,
            self.data_collected_file
        )

        current_timesteps = self.model.num_timesteps
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Guardar modelo con un nombre que indica los timesteps entrenados
        model_name = "model_final.zip" if final else "model"
        model_path = os.path.join(self.model_dir, model_name)
        self.model.save(model_path)

        if self.verbose > 0:
            print(f"[SaveOnRolloutCallback] Modelo guardado en: {model_path}")

        # **Leer el valor anterior de los timesteps entrenados para sumarlos**
        previous_timesteps = 0
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r") as f:
                    checkpoint_data = json.load(f)
                    previous_timesteps = checkpoint_data.get("timesteps_trained", 0)  # Cargar los timesteps previos
            except Exception as e:
                print(f"[WARNING] No se pudo leer el JSON, reiniciando los timesteps: {e}")
                previous_timesteps = 0

        # **Sumar los nuevos timesteps al valor previo**
        total_timesteps = previous_timesteps + current_timesteps

        # Guardar checkpoint con el número de timesteps entrenados
        checkpoint_data = {
            "timesteps_trained": int(total_timesteps),
            "last_save_time": timestamp_str
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)
